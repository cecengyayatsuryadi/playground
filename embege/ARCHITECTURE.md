# Arsitektur Aplikasi Makan Bergizi Gratis (MBG) / SPPG

Dokumen ini menjelaskan rancangan arsitektur untuk sistem operasional dan administratif dapur MBG (Makan Bergizi Gratis).

## 1. Tinjauan Sistem (System Overview)

Sistem ini melayani dua domain fungsional utama:
*   **Administratif (Owner/Manajemen Pusat):** Digunakan untuk mengawasi seluruh cabang, melihat laporan, manajemen stok global, pencatatan keuangan, dan master data (resep, bahan baku, karyawan).
*   **Operasional (Staf Dapur Cabang):** Digunakan untuk aktivitas harian di setiap dapur cabang, seperti penerimaan bahan baku (inbound), pencatatan produksi (cooking), pengemasan (packing), hingga distribusi (outbound/delivery), serta absensi harian.

Sistem ini didesain **Multi-Cabang (Multi-tenant)** dengan satu _backend_ tersentralisasi namun di-_deploy_ secara **lokal** (Local Server / On-Premise) menggunakan Docker.

## 2. Stack Teknologi Terpilih

Berdasarkan kebutuhan yang diuraikan, berikut adalah tumpukan teknologi (Tech Stack) yang akan digunakan:

### A. Frontend Web (Administratif - Owner & Admin Cabang)
*   **Framework:** Next.js (React Framework)
*   **Styling & UI Components:** Tailwind CSS + shadcn/ui
*   **Peruntukan:** Dashboard Owner, Laporan Konsolidasi Multi-Cabang, Master Data, Manajemen Pengguna.
*   **Akses:** Mengakses API Backend via HTTP/REST (atau gRPC-Web jika dibutuhkan).

### B. Frontend Mobile (Operasional - Staf Dapur & Kurir)
*   **Framework:** Flutter (Android)
*   **Peruntukan:** Pencatatan operasional harian (Checklist memasak, scan QR/Barcode bahan baku, absensi, update status pengiriman).
*   **Akses:** Mengakses API Backend via HTTP/REST. Jika server _backend_ berada di jaringan lokal (LAN/WiFi), device Android harus terhubung ke jaringan WiFi yang sama.

### C. Backend (Core API & Business Logic)
*   **Bahasa Pemrograman:** Go (Golang)
*   **Arsitektur Aplikasi:** Modular Monolith (Clean Architecture atau Domain-Driven Design disarankan).
    *   _Mengapa Modular Monolith?_ Lebih mudah di-deploy ke _local server_ menggunakan Docker Compose dibandingkan Microservices, namun tetap menjaga isolasi kode (modul stok, modul produksi, modul HR) untuk kemudahan _maintenance_.
*   **API Protocol:** RESTful JSON (menggunakan _router_ ringan seperti Echo, Gin, atau Chi).

### D. Database & Penyimpanan
*   **Relational Database:** PostgreSQL
*   **Model Multi-tenant:** **Logical Separation (Row-level Isolation)**
    *   Satu _database cluster_, satu _schema_, namun setiap tabel transaksi memiliki kolom `branch_id`.
    *   _Mengapa?_ Lebih mudah mengelola laporan agregat (konsolidasi) untuk Owner karena semua data berada di tabel yang sama.

### E. Infrastruktur & Deployment (Local Docker)
*   **Containerization:** Docker & Docker Compose.
*   **Komponen Docker Compose:**
    1.  `app` (Go Binary)
    2.  `db` (PostgreSQL 15+)
    3.  `proxy` (Nginx/Traefik) - Untuk _reverse proxy_ dan SSL termination (jika lokal ingin dipublikasikan via IP Publik/VPN).

---

## 3. Topologi Deployment Lokal (Local On-Premise Topology)

Mengingat kebutuhan Anda adalah **Backend Lokal** namun mendukung **Multi-Cabang**, ada beberapa pendekatan arsitektur _deployment_:

### Rekomendasi: Pendekatan Centralized "Local" Server (Headquarters Hosted)
Server fisik diletakkan di **Kantor Pusat / Dapur Induk**, dijalankan via Docker.
*   **Cabang Induk:** Mengakses server secara lokal (LAN/WiFi). Sangat cepat.
*   **Cabang Lain (Remote):** Mengakses server tersebut melalui **VPN (Virtual Private Network)** (seperti Tailscale atau WireGuard) **ATAU** server lokal diberi **Public Static IP** (atau layanan _tunneling_ seperti Cloudflare Tunnels).
*   **Keuntungan:** Data real-time untuk Owner. Aplikasi Web (Next.js) Owner selalu mendapatkan data terkini. Tidak perlu sinkronisasi data antar cabang.
*   **Kelemahan:** Jika internet di server pusat mati, cabang lain tidak bisa _input_ data (kecuali Flutter dibuat _Offline-First_).

*(Alternatif: Decentralized Edge Servers - Sangat kompleks karena butuh replikasi data dari setiap PostgreSQL cabang ke Server Pusat Owner setiap malam).*

---

## 4. Struktur Modul Aplikasi

### A. Modul Master Data
*   `Users & Roles`: Manajemen hak akses (Owner, Admin Cabang, Koki Utama, Kurir).
*   `Branches`: Manajemen data cabang SPPG.
*   `Items & Recipes`: Database bahan baku, kemasan, dan resep standar (Bill of Materials/BOM).

### B. Modul Operasional Dapur (Fokus Flutter)
*   `Inventory (Inbound/Outbound)`: Mencatat kedatangan bahan baku dari *supplier*, dan pengeluaran bahan ke dapur.
*   `Production/Cooking`: Jadwal masak harian, target jumlah *porsi*, dan realisasi.
*   `Packaging`: Proses _quality control_ dan _packing_ makanan jadi.
*   `Distribution`: Jadwal rute pengiriman ke sekolah/target, update status _delivered_.
*   `Attendance`: Absensi staf dapur/kurir.

### C. Modul Administratif & Laporan (Fokus Next.js)
*   `Dashboard`: Ringkasan status produksi hari ini per cabang, status pengiriman.
*   `Financials (Simple)`: Pencatatan harga beli bahan baku (HPP/COGS) vs budget.
*   `Consolidated Reports`: Export laporan produksi dan stok dalam format PDF/Excel.

---

## 5. Skema Database Multi-Tenant (Contoh)

Pemisahan data per cabang dilakukan di level *query*, di mana setiap *query* dari cabang akan di-*filter* berdasarkan JWT Token pengguna yang _login_.

**Contoh Tabel (Pseudo-schema):**

```sql
-- Tabel Cabang
CREATE TABLE branches (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    created_at TIMESTAMP
);

-- Tabel Pengguna
CREATE TABLE users (
    id UUID PRIMARY KEY,
    branch_id UUID REFERENCES branches(id), -- Null jika user adalah Owner (Superadmin)
    role VARCHAR(50), -- 'owner', 'branch_admin', 'chef', 'courier'
    name VARCHAR(255),
    password_hash VARCHAR(255)
);

-- Tabel Transaksi Produksi (Memiliki branch_id)
CREATE TABLE daily_productions (
    id UUID PRIMARY KEY,
    branch_id UUID REFERENCES branches(id) NOT NULL,
    target_date DATE NOT NULL,
    recipe_id UUID REFERENCES recipes(id),
    target_portions INT,
    actual_portions INT,
    status VARCHAR(50) -- 'planned', 'cooking', 'done'
);
```

### Mekanisme Pengamanan (Security)
Backend Go akan membaca `branch_id` dari _claims_ JWT.
Jika _Role_ = `branch_admin`, maka sistem otomatis menambahkan `WHERE branch_id = ?` ke setiap *query* database.
Jika _Role_ = `owner`, *query* tidak di-_filter_ (atau _filter_ bersifat opsional di UI).

---

## 6. Diagram Alur (High-Level)

```text
[Aplikasi Operasional]            [Aplikasi Administratif]
Flutter (Android)                 Next.js + shadcn/ui (Web)
        |                                     |
        |  (JSON / REST API over HTTP/S)      |
        v                                     v
+-------------------------------------------------------------+
|                     DOCKER HOST (Lokal)                     |
|                                                             |
|  +-------------------------------------------------------+  |
|  | Nginx / Reverse Proxy (Port 80/443)                   |  |
|  +-------------------------------------------------------+  |
|                           |                                 |
|                           v                                 |
|  +-------------------------------------------------------+  |
|  | GO BACKEND APP (Port 8080)                            |  |
|  | - Auth Middleware (JWT & Role/Tenant Checking)        |  |
|  | - Business Logic (Stok, Produksi, Distribusi)         |  |
|  +-------------------------------------------------------+  |
|                           |                                 |
|                           v                                 |
|  +-------------------------------------------------------+  |
|  | PostgreSQL DATABASE (Port 5432)                       |  |
|  | - Semua schema dengan kolom `branch_id`               |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
```

## Langkah Selanjutnya (Next Steps)

1.  **Validasi Struktur Database:** Menyusun _Entity-Relationship Diagram_ (ERD) lengkap berdasarkan modul di atas.
2.  **Inisiasi Proyek (Scaffolding):**
    *   Membuat repositori untuk Go Backend (termasuk *Dockerfile* & *docker-compose.yml*).
    *   Membuat repositori untuk Next.js Web (setup Tailwind & shadcn).
    *   Membuat repositori untuk Flutter Mobile.
3.  **Pengembangan API Inti:** Mulai dari modul Auth (Login/JWT) dan Master Data (Cabang & Pengguna).

---

## 7. Desain Skema Database (ERD Lengkap Terstruktur)

Sistem ini menggunakan arsitektur **Logical Separation** untuk *multi-tenant*, yang mana hampir seluruh tabel transaksional (kecuali referensi master global) akan memiliki kolom `branch_id` untuk memastikan pemisahan data setiap dapur cabang.

Berikut adalah rancangan awal struktur tabel PostgreSQL yang esensial untuk operasional SPPG:

### A. Modul Master Data (Global & Cabang)

```sql
-- 1. Cabang Dapur SPPG
CREATE TABLE branches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Pengguna & Karyawan Dapur (Multi-tenant: Jika Owner, branch_id = NULL)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) ON DELETE SET NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, -- Enum: 'owner', 'branch_admin', 'chef', 'warehouse_staff', 'courier'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Supplier / Pemasok Bahan Baku (Global)
CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(100),
    phone_number VARCHAR(50),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Target Distribusi / Sekolah Penerima (Bisa spesifik per cabang)
CREATE TABLE distribution_targets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) NOT NULL,
    name VARCHAR(255) NOT NULL, -- Nama Sekolah/Panti
    address TEXT,
    contact_person VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### B. Modul Operasional Dapur & Resep (Master Menu)

```sql
-- 5. Kategori Bahan Baku
CREATE TABLE item_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL -- Contoh: Sayuran, Daging, Bumbu, Kemasan
);

-- 6. Master Bahan Baku & Kemasan (Global)
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID REFERENCES item_categories(id),
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    unit_of_measure VARCHAR(20) NOT NULL, -- Kg, Liter, Pcs, Gram
    is_active BOOLEAN DEFAULT TRUE
);

-- 7. Master Menu / Resep Makanan (Global)
CREATE TABLE menus (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    calories_estimate INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Komposisi Resep / Bill of Materials (BOM) per 1 Porsi
CREATE TABLE menu_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_id UUID REFERENCES menus(id) ON DELETE CASCADE,
    item_id UUID REFERENCES items(id) NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL, -- Jumlah pemakaian bahan baku
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### C. Modul Perencanaan Menu (Menu Planning)

```sql
-- 9. Jadwal Menu Mingguan/Harian per Cabang (Multi-tenant)
CREATE TABLE menu_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) NOT NULL,
    target_date DATE NOT NULL,
    menu_id UUID REFERENCES menus(id) NOT NULL,
    meal_type VARCHAR(50), -- Enum: 'breakfast', 'lunch', 'dinner'
    target_portions INT NOT NULL DEFAULT 0, -- Target jumlah masak porsi
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### D. Modul Inventaris & Stok Gudang Cabang

```sql
-- 10. Stok Barang per Cabang (Multi-tenant)
CREATE TABLE branch_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) NOT NULL,
    item_id UUID REFERENCES items(id) NOT NULL,
    current_stock DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (branch_id, item_id) -- 1 barang 1 baris per cabang
);

-- 11. Transaksi Inbound (Penerimaan dari Supplier) / Outbound (Pemakaian)
CREATE TABLE inventory_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) NOT NULL,
    item_id UUID REFERENCES items(id) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- Enum: 'IN' (Penerimaan), 'OUT' (Pemakaian dapur), 'ADJUSTMENT' (Penyesuaian)
    quantity DECIMAL(10, 2) NOT NULL,
    supplier_id UUID REFERENCES suppliers(id), -- Jika penerimaan ('IN')
    reference_number VARCHAR(100), -- Nomor PO/Surat Jalan
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### E. Modul Produksi (Cooking & Packing)

```sql
-- 12. Rekap Produksi Harian (Berdasarkan Jadwal Menu)
CREATE TABLE daily_productions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) NOT NULL,
    schedule_id UUID REFERENCES menu_schedules(id) NOT NULL,
    status VARCHAR(50) NOT NULL, -- Enum: 'planned', 'cooking', 'quality_check', 'packed', 'ready_to_ship'
    actual_portions_cooked INT DEFAULT 0, -- Jumlah matang aktual
    actual_portions_packed INT DEFAULT 0, -- Jumlah yg berhasil dikemas
    notes TEXT,
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Jurnal Pemakaian Bahan Baku Aktual Harian (Berapa yang real-nya terpakai)
-- Tabel ini opsional jika stok langsung dipotong berdasarkan BOM (Menu Ingredients)
CREATE TABLE production_material_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    production_id UUID REFERENCES daily_productions(id) ON DELETE CASCADE,
    item_id UUID REFERENCES items(id) NOT NULL,
    actual_quantity_used DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### F. Modul Distribusi & Pengiriman (Delivery)

```sql
-- 14. Jadwal Pengiriman ke Sekolah/Target
CREATE TABLE deliveries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) NOT NULL,
    target_id UUID REFERENCES distribution_targets(id) NOT NULL,
    production_id UUID REFERENCES daily_productions(id), -- Mengirim produksi yang mana
    courier_id UUID REFERENCES users(id), -- User kurir (Flutter)
    delivery_date DATE NOT NULL,
    total_portions INT NOT NULL,
    status VARCHAR(50) NOT NULL, -- Enum: 'pending', 'on_the_way', 'delivered', 'failed'
    proof_of_delivery_url VARCHAR(255), -- Foto/Tanda tangan dari app Flutter
    delivered_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### G. Modul HR / Absensi Karyawan (Attendance)

```sql
-- 15. Kehadiran Karyawan (Staf Dapur/Kurir)
CREATE TABLE employee_attendances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    branch_id UUID REFERENCES branches(id) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    attendance_date DATE NOT NULL,
    check_in_time TIMESTAMP,
    check_in_location VARCHAR(255), -- GPS/Location atau IP
    check_in_photo_url VARCHAR(255), -- Selfie (Flutter)
    check_out_time TIMESTAMP,
    status VARCHAR(20), -- Enum: 'present', 'absent', 'sick', 'leave'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, attendance_date) -- 1 user 1 hari 1 absensi
);
```

---

## 8. Relasi Kunci (Key Constraints)
1. Setiap cabang (Branch) bertindak sebagai penyekat (Tenant). Oleh karena itu, *Branch Admin* (Web) dan Staf (Mobile) tidak akan dapat membaca/menulis data di luar `branch_id` mereka sendiri. Data ini divalidasi dan dilempar secara otomatis melalui parameter **JWT (JSON Web Token)** ketika *user* melakukan otentikasi.
2. Owner / Superadmin akan masuk dengan JWT yang mengidentifikasi peran sebagai `owner`, yang mana parameter pencarian di sisi Backend (Go) mengabaikan filter *branch_id* (bisa melihat semua cabang/Global).
3. Tabel seperti `menus`, `items`, `item_categories`, dan `suppliers` biasanya bersifat **Global/Master** agar standar MBG seragam antar cabang, maka mereka tidak terikat oleh `branch_id`. Namun, persediaan real-time seperti `branch_inventory` dipisah berdasarkan `branch_id`.
