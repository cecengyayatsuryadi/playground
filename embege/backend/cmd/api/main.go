package main

import (
	"log"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/joho/godotenv"
	"github.com/username/embege/backend/internal/config"
)

func main() {
	// Load .env file if it exists (for local development)
	_ = godotenv.Load()

	// Connect to the database
	db := config.ConnectDB()
	defer db.Close()

	// Initialize the router
	r := chi.NewRouter()

	// Use standard middlewares
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	// Define a simple health check route
	r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("MBG API is healthy and running!"))
	})

	// Get the port from the environment variable, or use 8080 by default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Starting MBG server on port :%s...\n", port)
	err := http.ListenAndServe(":"+port, r)
	if err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
