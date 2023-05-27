# input
name = input("What is your name? ")
print("Hello " + name)

# output
print("Hello World")
print("Hello", "World")
print("Hello", "World", sep=" ")
print("Hello", "World", sep=" - ")
print("Hello", "World", sep=" - ", end="!")
print("Hello", "World", sep=" - ", end="!\n")
print("Hello", "World", sep=" - ", end="!\n", flush=True)
print("Hello", "World", sep=" - ", end="!\n", flush=False)

# output format
print("Hello %s" % "World")
print("Hello %s" % ("World"))
print("Hello %s" % ("World",))
print("Hello %s" % ("World", "World"))
print("Hello %s" % ("World", "World", "World"))
