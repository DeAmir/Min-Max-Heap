"""
The skeleton of the program. Makes an interface for the user to create and manage a max-min heap.
Create a new heap and tries to load values from a file to it, using LoadFileHeap.
Uses the Runner class with that heap to operate.
"""

from InputManager import *

heap = MNHeap()
LoadFileHeap(heap)

# heap is empty if no file was given or an error occurred.
runner = Runner(heap)
while runner.getAlive():  # isn't alive once fetched EXIT action
    runner.showMenu()
    runner.fetchAction()
    runner.runAction()

print("Goodbye :)")
