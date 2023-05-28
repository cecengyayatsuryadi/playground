# for loop
for i in range(10):
    print(i)

# while loop
i = 0
while i < 10:
    print(i)
    i += 1

# while loop with break
i = 0
while True:
    print(i)
    i += 1
    if i >= 10:
        break

# while loop with continue
i = 0
while True:
    i += 1
    if i % 2 == 0:
        continue
    print(i)
    if i >= 10:
        break

# while loop with else
i = 0
while i < 10:
    print(i)
    i += 1
else:
    print("loop ended")

# for loop with else
for i in range(10):
    print(i)
else:
    print("loop ended")

# for loop with break
for i in range(10):
    print(i)
    if i >= 5:
        break
else:
    print("loop ended")

# for loop with continue
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)
else:
    print("loop ended")

# for loop with break and continue
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)
    if i >= 5:
        break
else:
    print("loop ended")
