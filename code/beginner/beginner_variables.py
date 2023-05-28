# Variables are containers for storing data values.
# Unlike other programming languages, Python has no command for declaring a variable.
# A variable is created the moment you first assign a value to it.

# Example
x = 5
y = "John"
print(x)
print(y)

# Variables do not need to be declared with any particular type and can even change type after they have been set.
# Example
x = 4 # x is of type int
x = "Sally" # x is now of type str
print(x)

# String variables can be declared either by using single or double quotes:
# Example
x = "John"
# is the same as
x = 'John'

# Variable Names
# A variable can have a short name (like x and y) or a more descriptive name (age, carname, total_volume).
# Rules for Python variables:
# A variable name must start with a letter or the underscore character
# A variable name cannot start with a number
# A variable name can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )
# Variable names are case-sensitive (age, Age and AGE are three different variables)

# Legal variable names:
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

# Illegal variable names:
# 2myvar = "John"
# my-var = "John"
# my var = "John"

# Assign Value to Multiple Variables
# Python allows you to assign values to multiple variables in one line:
# Example
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

# And you can assign the same value to multiple variables in one line:
# Example
x = y = z = "Orange"
print(x)
print(y)
print(z)

# Output Variables
# The Python print statement is often used to output variables.
# To combine both text and a variable, Python uses the + character:
# Example
x = "awesome"
print("Python is " + x)

# You can also use the + character to add a variable to another variable:
# Example
x = "Python is "
y = "awesome"
z =  x + y
print(z)

# For numbers, the + character works as a mathematical operator:
# Example
x = 5
y = 10
print(x + y)

# If you try to combine a string and a number, Python will give you an error:
# Example
x = 5
y = "John"
print(x + y)

# Global Variables
# Variables that are created outside of a function (as in all of the examples above) are known as global variables.
# Global variables can be used by everyone, both inside of functions and outside.
# Example
x = "awesome"
def myfunc():
    print("Python is " + x)
myfunc()

# If you create a variable with the same name inside a function, this variable will be local,
# and can only be used inside the function. The global variable with the same name will remain as it was,
# global and with the original value.
# Example
x = "awesome"
def myfunc():
    x = "fantastic"
    print("Python is " + x)
myfunc()
print("Python is " + x)

# The global Keyword
# Normally, when you create a variable inside a function, that variable is local, and can only be used inside that function.
# To create a global variable inside a function, you can use the global keyword.
# Example
def myfunc():
    global x
    x = "fantastic"
myfunc()
print("Python is " + x)

# Also, use the global keyword if you want to change a global variable inside a function.
# Example
x = "awesome"
def myfunc():
    global x
    x = "fantastic"
myfunc()
print("Python is " + x)

# To change the value of a global variable inside a function, refer to the variable by using the global keyword:
# Example
x = "awesome"
def myfunc():
    global x
    x = "fantastic"
myfunc()
print("Python is " + x)

# Python Data Types
# Built-in Data Types
# In programming, data type is an important concept.
# Variables can store data of different types, and different types can do different things.
# Python has the following data types built-in by default, in these categories:
# Text Type:	str
# Numeric Types:	int, float, complex
# Sequence Types:	list, tuple, range
# Mapping Type:	dict
# Set Types:	set, frozenset
# Boolean Type:	bool
# Binary Types:	bytes, bytearray, memoryview

# Getting the Data Type
# You can get the data type of any object by using the type() function:
# Example
x = 5
print(type(x))

# Setting the Data Type
# In Python, the data type is set when you assign a value to a variable:
# Example
x = "Hello World"	# str
x = 20	# int
x = 20.5	# float
x = 1j	# complex
x = ["apple", "banana", "cherry"]	# list
x = ("apple", "banana", "cherry")	# tuple
x = range(6)	# range
x = {"name" : "John", "age" : 36}	# dict
x = {"apple", "banana", "cherry"}	# set
x = frozenset({"apple", "banana", "cherry"})	# frozenset
x = True	# bool
x = b"Hello"	# bytes
x = bytearray(5)	# bytearray
x = memoryview(bytes(5))	# memoryview

# Setting the Specific Data Type
# If you want to specify the data type, you can use the following constructor functions:
# Example
x = str("Hello World")	# str
x = int(20)	# int
x = float(20.5)	# float
x = complex(1j)	# complex
x = list(("apple", "banana", "cherry"))	# list
x = tuple(("apple", "banana", "cherry"))	# tuple
x = range(6)	# range
x = dict(name="John", age=36)	# dict
x = set(("apple", "banana", "cherry"))	# set
x = frozenset(("apple", "banana", "cherry"))	# frozenset
x = bool(5)	# bool
x = bytes(5)	# bytes
x = bytearray(5)	# bytearray
x = memoryview(bytes(5))	# memoryview
