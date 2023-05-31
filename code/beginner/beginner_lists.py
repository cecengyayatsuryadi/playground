# lists python example beginner levels
# Date: 2021/04/18

# list
# list is a collection which is ordered and changeable. Allows duplicate members.
# list is a collection which is ordered and unchangeable. Allows duplicate members.
# list is a collection which is unordered and unindexed. No duplicate members.

# create a list
thislist = ["apple", "banana", "cherry"]
print(thislist)

# access items
thislist = ["apple", "banana", "cherry"]
print(thislist[1])

# negative indexing
thislist = ["apple", "banana", "cherry"]
print(thislist[-1])

# range of indexes
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])

# range of negative indexes
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[-4:-1])

# change item value
thislist = ["apple", "banana", "cherry"]
thislist[1] = "blackcurrant"
print(thislist)

# loop through a list
thislist = ["apple", "banana", "cherry"]
for x in thislist:
    print(x)

# check if item exists
thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
    print("Yes, 'apple' is in the fruits list")

# list length
thislist = ["apple", "banana", "cherry"]
print(len(thislist))

# add items
# append() - adds an element at the end of the list
thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

# insert() - adds an element at the specified position
thislist = ["apple", "banana", "cherry"]
thislist.insert(1, "orange")
print(thislist)

# remove items
# remove() - removes the specified item
thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)

# pop() - removes the specified index, (or the last item if index is not specified)
thislist = ["apple", "banana", "cherry"]
thislist.pop()
print(thislist)

# del - removes the specified index
thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist)

# del - deletes the entire list
thislist = ["apple", "banana", "cherry"]
del thislist

# clear() - empties the list
thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)

# copy() - returns a copy of the list
thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)

# list() - returns a copy of the list
thislist = ["apple", "banana", "cherry"]
mylist = list(thislist)
print(mylist)

# join two lists
# + operator
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]
list3 = list1 + list2
print(list3)

# append() method
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]
for x in list2:
    list1.append(x)
print(list1)

# extend() method
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]
list1.extend(list2)
print(list1)

# list() method
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]
list3 = list(list1)
for x in list2:
    list3.append(x)
print(list3)
