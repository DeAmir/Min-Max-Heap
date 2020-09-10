"""
This file contains an implementation of a max-min heap as an object. The heap holds integer numbers.
The object is named MNHeap (Min-Max-Heap).
It uses helper functions from the HelperFunctions.py file for index calculations and array management.
"""

from HelperFuncitions import *
import sys  # for maxint, used in heapDelete

# maximum heap length
MAX_LEN = 1000


class MNHeap:
    def __init__(self):
        self.heap = FixedArray(MAX_LEN)

    # checks index boundaries.
    def validIdx(self, i):
        return self.heap.validIdx(i)

    """
    Gets an index (idx) and a boolean is_max. returns (a,b,c,d) [a,b,c boolean values; d integer] where:
    a is True if A[idx] is bigger/lower than the closest minimum/maximum above it (grandpa), otherwise False;
    b is True if  A[idx] is lower/bigger than it's father;
    c is True if A[idx] is the lowest/biggest in the subtree rotted at it, otherwise False;
    d is the index lowest/biggest item in subtree rotted at A[idx]. -1 if it's idx.
    the left option is chosen is is_max=False; if True, the right one.
    """

    def __getDepthInfo(self, idx, is_max):
        order = bigger if is_max else lower
        ordeq = lambda a, b: (order(a, b) or a == b)  # lower-equal/bigger-equal

        grand_relation = False  # =a; bigger/lower than grandpa
        papa_relation = False  # =b; lower/bigger
        subtree_relation = False  # =c is lowest/biggest in subtree
        wrong_gchild = -1  # =d index of minimum/maximum item in subtree

        A = self.heap

        if not self.validIdx(Parent(Parent(idx))) or ordeq(A[Parent(Parent(idx))], A[
            idx]):  # if doesn't have a grandpa of relation stands (grandpa lower/bigger equal to me)
            grand_relation = True
        if not self.validIdx(Parent(idx)) or ordeq(A[idx],
                                                   A[Parent(idx)]):  # if doesn't have a papa or papa relation stands
            papa_relation = True  # me lower/bigger equal papa

        if not self.validIdx(Left(idx)) and not self.validIdx(Right(idx)):  # if doesn't have sons
            subtree_relation = True  # nothing in subtree
        else:  # then must have left son
            wrong_gchild = Left(idx)
            if self.validIdx(Right(idx)) and order(A[Right(idx)], A[wrong_gchild]):  # get minimum/maximum of sons
                wrong_gchild = Right(idx)
            for i in range(Left(Left(idx)), Right(Right(idx)) + 1):  # gets minimum/maximum including grand-sons
                if not self.validIdx(i):
                    break
                if order(A[i], A[wrong_gchild]):
                    wrong_gchild = i

            if ordeq(A[idx], A[wrong_gchild]):  # if I am lower/bigger equal to minimum/maximum in subtree
                subtree_relation = True

        return grand_relation, papa_relation, subtree_relation, wrong_gchild

    """
    Gets an index (idx) and returns (a,b,c,d) [a,b,c boolean values; d integer] where:
    a is True if A[idx] is lower than the closest maximum above it (grandpa), otherwise False;
    b is True if  A[idx] is bigger than it's father;
    c is True if A[idx] is the biggest in the subtree rotted at it, otherwise False;
    d is the index biggest item in subtree rotted at A[idx]. -1 if no items in subtree.
    """

    def __getMaxDepthInfo(self, idx):
        return self.__getDepthInfo(idx, True)

    """
    Gets an index (idx) and a boolean is_max. returns (a,b,c,d) [a,b,c boolean values; d integer] where:
    a is True if A[idx] is bigger than the closest minimum above it (grandpa), otherwise False;
    b is True if  A[idx] is lower than it's father;
    c is True if A[idx] is the lowest in the subtree rotted at it, otherwise False;
    d is the index lowest item in subtree rotted at A[idx]. -1 if no items in subtree.
    """

    def __getMinDepthInfo(self, idx):
        return self.__getDepthInfo(idx, False)

    """
    does Max-Heapify on idx: assumes that idx is a valid index, in an even depth in the heap.
    assumes that when looking at the heap without A[idx], all items answer the max-min heap demand.
    the function moves A[idx] to a place where the whole heap is valid.
    gets a boolean down_only which declares whether to only check disorder down of A[idx].
    """

    def __maxHeapify(self, idx, down_only=False):
        A = self.heap
        (lower_than_max, papa_is_lower, biggest_in_subtree, max_below) = self.__getMaxDepthInfo(idx)

        if down_only:
            lower_than_max = papa_is_lower = True  # skip to last case

        if not lower_than_max:  # case (1)
            max_up = Parent(Parent(idx))
            switchItems(A, max_up, idx)  # switch with grandpa and run recursively on grandpa
            self.__maxHeapify(max_up)  # only he might not obey max-min
        # now lower_than_max is True.
        elif not papa_is_lower:  # case (2)
            switchItems(A, idx, Parent(idx))
            self.__minHeapify(Parent(idx))  # fix dad first; goes up the tree
            self.__maxHeapify(idx)  # fix current item; goes down the tree

        # now now lower_than_max=papa_is_lower=True
        elif not biggest_in_subtree:  # case (3)
            # then max_below isn't -1
            switchItems(A, idx, max_below)  # switch with maximum. after the switch A[idx] is valid.
            if isEvenDepth(max_below):  # A[max_below] might not be
                self.__maxHeapify(max_below, False)  # go down the tree
            # else then it's a leaf. obeys max-min.
        # no problem, do nothing

    """
    does Max-Heapify on idx: assumes that idx is a valid index, in an odd depth in the heap.
    assumes that when looking at the heap without A[idx], all items answer the max-min heap demand.
    the function moves A[idx] to a place where the whole heap is valid.
    gets a boolean down_only which declares whether to only check disorder down of A[idx].
    """

    def __minHeapify(self, idx, down_only=False):
        A = self.heap
        (bigger_than_min, papa_is_bigger, lowest_in_subtree, min_below) = self.__getMinDepthInfo(idx)

        if down_only:
            bigger_than_min = papa_is_bigger = True

        if not bigger_than_min:  # case (1)
            min_above = Parent(Parent(idx))
            switchItems(A, min_above, idx)
            self.__minHeapify(min_above)  # A[idx] is valid; A[min_above] might not be
        elif not papa_is_bigger:  # case (2)
            switchItems(A, idx, Parent(idx))
            self.__maxHeapify(Parent(idx))  # fix dad first; goes up
            self.__minHeapify(idx)  # fix current item; does down the tree
        elif not lowest_in_subtree:  # case (3)
            switchItems(A, idx, min_below)
            if not isEvenDepth(min_below):  # A[idx] is valid; A[min_below] might not be
                self.__minHeapify(min_below)

    """
    assumes that when looking at the heap without A[idx], all items answer the max-min heap demand.
    gets an index of an item in the heap that might make disorder and fixes it using Min/Max heapify, based on it's depth.
    gets a boolean down_only which declares whether to only check disorder down of A[idx].
    """

    def __heapify(self, idx, down_only=False):
        # operate based on depth
        if isEvenDepth(idx):
            self.__maxHeapify(idx, down_only)
        else:
            self.__minHeapify(idx, down_only)

    # gets an array of integers.
    # sets current heap to a new heap containing the array values
    def buildHeap(self, arr):
        if not self.heap.copyToBegg(arr):
            return False

        first_not_leaf = math.floor(len(self) / 2)  # equals whats in the book, minus 1 (indexes start at 0)
        i = first_not_leaf
        while self.validIdx(i):
            self.__heapify(i, down_only=True)  # only go down
            i -= 1
        return True

    # returns and removes the maximum item in the heap.
    # returns None if the list is empty, otherwise the maximum.
    def heapExtractMax(self):
        A = self.heap
        if len(A) == 0:
            return None

        maxi = A[0]  # the maximum is the root
        switchItems(A, 0, len(A) - 1)
        A.removeLast()

        # now only A[0] might rebel max-min
        if self.validIdx(0):  # might extracted the root, check
            self.__heapify(0, down_only=True)  # root might only go down

        return maxi

    # removes the minimum item in the heap.
    # if list is empty, returns None. Otherwise, the minimum.
    def heapExtractMin(self):
        A = self.heap
        if len(A) == 0:
            return None
        min_idx = 0
        if self.validIdx(1) and A[1] < A[min_idx]:  # left son check
            min_idx = 1
        if self.validIdx(2) and A[2] < A[min_idx]:  # right son check
            min_idx = 2
        # A[min_idx] now contains the minimum

        minval = A[min_idx]  # save value

        switchItems(A, min_idx, len(A) - 1)
        A.removeLast()

        # now A[min_idx] is the only one that might rebel max-min
        if self.validIdx(min_idx):
            self.__heapify(min_idx)  # not a root - could go up or down

        return minval

    # gets an integer and adds it to the heap.
    def heapInsert(self, key):
        A = self.heap
        if not A.append(key):
            return False
        # now only the last item might rebel max-min
        self.__heapify(len(self) - 1)
        return True

    # gets an index and removes the item at that index from the heap.
    def heapDelete(self, idx):
        A = self.heap
        A[idx] = sys.maxsize  # now it's the maximum in the heap; only it rebels
        self.__heapify(idx)  # moves it to the root
        self.heapExtractMax()  # removes it

    # gets an array and does heap sort on it, keeping the ordered list at self.heap.
    def heapSort(self, arr):
        self.buildHeap(arr)
        A = self.heap
        ln = len(arr)
        # fill with maximums from end to start
        for i in range(len(self)):
            switchItems(A, 0, len(A) - 1)
            A.removeLast()
            self.__heapify(0)

        A.setFree(ln)  # so we could see changes

    # for printing purposes
    def __repr__(self):
        return str(self.heap)

    # object length management functions
    def __len__(self):
        return len(self.heap)
