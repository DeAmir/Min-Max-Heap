"""
This file is responsible for input management in the program.
The main.py file uses the Runner class to run the program.
"""

from MNHeap import *


# the Runner class.
# the 'alive' attribute of it is a term for the main loop in main.py.
# initializer: gets a valid MNHeap as an input.
class Runner:
    def __init__(self, heap):
        self.__heap = heap
        self.__alive = True  # sign for main.py
        self.__actionrng = Actions.all_range if self.__heapBuilt() else Actions.base_range  # action ranges based on heap emptyness
        self.__show_menu = True
        self.__action = Actions.BUILD_HEAP  # just for not exiting on fetch action at first
        self.__valid_action = True

    # returns True is heap isn't empty otherwise False
    def __heapBuilt(self):
        return len(self.__heap) > 0

    # shows menu based on class parameters
    def showMenu(self):
        if self.__show_menu:
            self.__show_menu = False
            self._printBaseMenu()
            if self.__heapBuilt():  # only then, the other actions are allowed
                self.__printRestOfMenu()

    # sets self.action to a user given action. sets the self.valid_action sign accordingly.
    def fetchAction(self):
        self.__action = self.__getUserInt("> ")
        if self.__validStrAction() or self.__validIntAction():
            self.__valid_action = True
        else:
            self.__valid_action = False

    # runs the action in self.action while manipulating class parameters accordingly.
    def runAction(self):
        if not self.__valid_action or IsStr(self.__action):  # skip invalid and string actions
            return

        # now action is an integer
        was_empty_before = not self.__heapBuilt()
        if self.__operateOnHeap() and was_empty_before:  # True if Heap contains elements after the action and heap was empty before
            self.__show_menu = True  # show extended menu
            self.__actionrng = Actions.all_range  # all actions permitted

        if not self.__heapBuilt():  # if empty after action
            self.__show_menu = True  # show limited menu
            self.__actionrng = Actions.base_range

    # valid str actions are '' and 'help' (case doesn't matter). returns True if self.action is string and valid.
    # if action is 'help' then set show_menu to True, to present the menu later.
    def __validStrAction(self):
        if IsStr(self.__action):  # check if valid string operation
            if self.__action.lower() == "help":  # ignore capitality of case
                self.__show_menu = True
                return True
            elif self.__action == '':  # skip whitespaces lines
                return True
        return False

    # returns True if  self.action is valid else False, and prints error message accordingly.
    def __validIntAction(self):
        if not self.__action in self.__actionrng:
            print("Error: invalid action '%s'. Should be a number in range %d to %d." % (
                str(self.__action), self.__actionrng[0], self.__actionrng[-1]))
            return False
        return True

    # gets a MNHeap and an integer action that's in the current valid action range. Does the appropriate action on the heap.
    # returns True if the heap isn't empty after the action.
    def __operateOnHeap(self):
        if self.__action == Actions.EXIT:
            self.__alive = False
        elif self.__action == Actions.BUILD_HEAP:
            self.__buildUserHeap()
        elif self.__action == Actions.PRINT_HEAP:
            print(self.__heap)
        elif self.__action == Actions.HEAPEX_MAX:
            if len(self.__heap) < 1:
                print("Heap is empty, can't extract.")
            else:
                m = self.__heap.heapExtractMax()
                print("Extracted maximum %d. New heap:" % m)
                print(self.__heap)
        elif self.__action == Actions.HEAPEX_MIN:
            if len(self.__heap) < 1:
                print("Heap is empty, can't extract.")
            else:
                m = self.__heap.heapExtractMin()
                print("Extracted minimum %d. New heap:" % m)
                print(self.__heap)
        elif self.__action == Actions.HEAP_INS:
            key = self.__getUserInt("Put value to insert: ")
            if IsStr(key):
                print("Invalid index '%s' - not a number." % key)
            elif key == sys.maxsize:
                print("Invalid number: The number %d shouldn't be used. Put numbers below it." % key)
            else:
                self.__heap.heapInsert(key)
        elif self.__action == Actions.HEAP_DEL:
            idx = self.__getUserInt("Put index of an item to delete: ")
            if IsStr(idx):
                print("Invalid index '%s' - not a number." % idx)
            elif not self.__heap.validIdx(idx):
                print("Invalid index %d - not in range." % idx)
            else:
                self.__heap.heapDelete(idx)
        elif self.__action == Actions.HEAPSORT:
            self._userHeapsort()

        return len(self.__heap) > 0

    # Heapsort option for the user. The user could choose to HeapSort the current active heap, but it will destroy it.
    # He could also choose to create a temporary heap from new value to be given, and on that heap to do the sorting.
    # returns nothing.
    def _userHeapsort(self):
        action = self.__getUserInt(
            "Options: \n\t\t(1) Heapsort this heap [DESTROYES THE HEAP].\n\t\t(2) Create a temporary heap just for sorting, and load given values to it.\n\t\t>>>")
        if IsStr(action) or not action in [1, 2]:
            print("\t\t Invalid action given.")
        elif action == 1:  # sort current heap
            self.__heap.heapSort(self.__heap.heap)
            print(self.__heap)
            print("Heap ruined. Create a new heap.")
            self.__heap.heap.setFree(0)  # signal that it's empty
        elif action == 2:
            # get values to sort
            st = input("Put values to sort: ").strip()
            vals = StrToList(st)
            if not type(vals) == Exception:
                tmp = MNHeap()  # sort on temporary heap
                tmp.heapSort(vals)
                print(tmp)
                del tmp

    # gets integers from the user from which to build self.heap.
    # Returns True on success, otherwise False.
    def __buildUserHeap(self):
        print("Put integers separated with spaces (all in a single line).")
        st = input(">>> ").strip()
        values = StrToList(st)
        if type(values) == Exception:
            return False

        self.__heap.buildHeap(values)
        return True

    # Menu printing methods
    def _printBaseMenu(self):
        print("""Options menu:
                1) Exit.
                2) Build Heap.
                """, end='')

    def __printRestOfMenu(self):
        print("""3) Print Heap.
                4) Extract Max.
                5) Extract Min.
                6) Insert.
                7) Delete.
                8) Heap-Sort.
                    """)
        print("Type 'help' (case doesn't matter) to show the menu again.")

    # gets a prompt that is shown when the function retrieves an integer from the command prompt.
    # returns the integer if it's valid. Otherwise returns the string the user gave.
    def __getUserInt(self, prompt):
        inp = input(prompt).strip()
        try:
            m = int(inp)
            return m
        except:
            return inp

    # getter method
    def getAlive(self):
        return self.__alive


# action constants and ranges
class Actions:
    EXIT = 1
    BUILD_HEAP = 2
    PRINT_HEAP = 3
    HEAPEX_MAX = 4  # EX=EXTRACT
    HEAPEX_MIN = 5
    HEAP_INS = 6
    HEAP_DEL = 7
    HEAPSORT = 8
    NUM_ACTIONS = 8

    base_range = [EXIT, BUILD_HEAP]  # used when heap is empty
    all_range = range(1, NUM_ACTIONS + 1)  # used when not


# gets an object and returns True is it's a string.
def IsStr(action):
    return type(action) == str


"""
gets a MNHeap object and checks if there is a filename in the command line arguments.
if so, it tries to load values from it into the heap, making a heap of the values in the file.
the file should be in the same directory as the python file.
the file should contain integers separated with spaces. if any errors occur, it will draw an error message.
"""


def LoadFileHeap(heap):
    fn = None
    fd = None
    if len(sys.argv) == 1:
        return
    fn = sys.argv[1]  # get filename

    try:
        fd = open(fn, "r")
        print("File opened successfully. Creating heap from values...")
        contents = fd.read()
        values = StrToList(contents)  # make a list of integers out of the file
        if type(values) == Exception:  # then error occurred (message already printed)
            print("Continuing on regular activity.")
        else:  # values are OK
            if heap.buildHeap(values):
                print("Heap loaded successfully.")
    except:  # error opening file
        if fd == None:
            print("Error: Couldn't open file %s." % fn)
            print("Continuing with regular activity.")
    finally:
        if fd != None:
            fd.close()


# gets a string containing space-separated integers, and crafts a list of those integers.
# returns an Exception if trouble-maker value is detected (if it's not a number, etc.).
# Otherwise returns the list of numbers.
def StrToList(st):
    strls = st.split()
    ret = None
    try:
        ret = [int(v) for v in strls]
    except Exception as e:
        print("Invalid value - ", e)
        return Exception()
    return ret
