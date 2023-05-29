# function with no arguments
def hello_world():
    print("Hello world!")


# function with one argument
def hello_name(name):
    print("Hello " + name)


# function with two arguments
def hello_name_age(name, age):
    print("Hello " + name + ", you are " + str(age) + " years old.")


# function with two arguments and return value
def hello_name_age_return(name, age):
    return "Hello " + name + ", you are " + str(age) + " years old."
