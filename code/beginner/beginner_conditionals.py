# if statement
if 5 > 2:
    print("Five is greater than two!")

# if else statement
if 5 > 2:
    print("Five is greater than two!")
else:
    print("Five is not greater than two!")

# if elif else statement
if 5 > 2:
    print("Five is greater than two!")
elif 5 == 2:
    print("Five is equal to two!")
else:
    print("Five is not greater than two!")

# short hand if statement
if 5 > 2:
    print("Five is greater than two!")

# short hand if else statement
print("Five is greater than two!") if 5 > 2 else print("Five is not greater than two!")

# short hand if elif else statement
print("Five is greater than two!") if 5 > 2 else print(
    "Five is equal to two!"
) if 5 == 2 else print("Five is not greater than two!")

# and operator
if 5 > 2 and 5 > 1:
    print("Both conditions are True!")

# or operator
if 5 > 2 or 5 > 1:
    print("At least one of the conditions is True!")

# nested if statement
x = 41
if x > 10:
    print("Above ten,")
    if x > 20:
        print("and also above twenty!")
    else:
        print("but not above twenty!")

# pass statement
if 5 > 2:
    pass

# if statement with multiple conditions
x = 41
if x > 10:
    print("Above ten,")
elif x > 20:
    print("and also above twenty!")
else:
    print("but not above twenty!")
