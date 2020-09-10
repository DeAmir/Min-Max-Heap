"""
This file contains helper functions for the MNHeap.py file.
Mostly index calculations.
"""
import math

# gets an index of an item in max-min heap and returns the left son's index.
def Left(i):
    return 2 * i + 1

# gets an index of an item in max-min heap and returns the right son's index.
def Right(i):
    return 2 * i + 2

# gets an index of an item in max-min heap and returns it's parent's index.
def Parent(i):
    return math.ceil(i / 2) - 1


# gets an index of an item in max-min heap and returns the depth of it.
def idx2depth(i):
    return math.floor(math.log2(i + 1))

# gets an index of an item in max-min heap and returns True if the depth is even, otherwise odd.
def isEvenDepth(i):
    return idx2depth(i) % 2 == 0

# gets an array and two indexes and exchanges them.
def switchItems(A, i, j):
    temp = A[i]
    A[i] = A[j]
    A[j] = temp


# order functions for depth info functions.
def bigger(a, b):
    return a > b


def lower(a, b):
    return a < b


# contains a fixed size int array and lets do actions on it
class FixedArray:

    # the fixed length is given as parameter
    def __init__(self, ln):
        self.arr = [int] * ln
        self.__ln = ln
        self.__free = 0  # next free spot

    # adds an int to the array. returns True on success, False otherwise
    def append(self, key):
        if self.__free >= self.__ln:
            print("Error Maximum length of %d has been reached" % self.__ln)
            return False

        self.arr[self.__free] = key
        self.__free += 1
        return True

    # like pop - removes the last element in the array
    def removeLast(self):
        if self.__free < 0:
            print("Array underflow. Exiting...")
            return False

        self.__free -= 1
        return True

    # checks if given index is in boundaries of the array
    def validIdx(self, i):
        return i >= 0 and i < self.__free

    # copies a given array to the beggining of the contained array
    # return True on success, otherwise False
    def copyToBegg(self, arr):
        if len(arr) > self.__ln:
            print("Error: Maximum length of %d has been reached." % self.__ln)
            return False
        self.__free = len(arr)
        self.arr[:self.__free] = arr
        return True

    # setter for __free
    def setFree(self, new):
        self.__free = new

    def __len__(self):
        return self.__free

    def __getitem__(self, item):  # so we could use [idx] on the object
        return self.arr[item]

    def __setitem__(self, key, value):
        self.arr[key] = value

    def __repr__(self):
        return str(self.arr[:self.__free])  # only whats in working sub-array
