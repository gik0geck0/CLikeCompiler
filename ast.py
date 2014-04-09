
from sys import exit

# Contains data structures for the abstract syntax tree, as well as the visitation rights

nextid = 0
# Abstract Node definition. It contains the bare minimum that ALL nodes must have
class Node:
    def __init__(self, kind, data=None, father=None, leftmostChild=None, leftmostSibling=None, rightSibling=None):
        self.kind = kind
        self.data = data
        global nextid
        self.simple_id = nextid
        nextid += 1

        # Traditionally, the term "parent" is used...
        # But I made a joke at the end of adoptChildren
        self.father = father
        self.leftmostChild = leftmostChild

        # This prevents None-checking when considering who the left-most sibling is
        if leftmostSibling is None:
            leftmostSibling = self

        self.leftmostSibling = leftmostSibling
        self.rightSibling = rightSibling

    def makeSiblings(self, siblingInRight):
        '''
        Joins two sibling lists. Designed to be callable with ANY node in either
        list.
        Returns a reference to self for easy chaining
        '''
        # Notation wise, we are joining the lists left and right. leftHead will
        # be the left-most sibling of the left-list, and rightHead will be the
        # head of the right-list

        # Normalize to the heads of each list
        leftHead = self.leftmostSibling
        rightHead = siblingInRight.leftmostSibling

        if leftHead is rightHead:
            # Our work is done. These two sibling lists are the same
            print("MakeSiblings: ShortCircuit because these nodes are already siblings")
            return self


        # Jump to the insertion point, shortening the seektime by starting at
        # this node, which is at worst case the head of the list
        # print("Getting rightMostSibling")
        leftTail = self.getRightMostSibling()

        # Join the lists by their ends
        # print("Joining the left tail %s with the right head %s" % (leftTail, rightHead))
        if leftTail is rightHead:
            print("Cannot join the two lists. The left tail is the right head. How did this happen?")
            leftHead.prettyPrintStructure()
            rightHead.prettyPrintStructure()
            exit(-1)
        leftTail.rightSibling = rightHead

        # Update the left-most sibling pointers
        # It doesn't matter which node is used to get all the siblings,
        # but we may as well use the originally passed in node
        for node in siblingInRight.getSiblings():
            # All nodes in the right list must have the same sibling-head as the left-list
            node.leftmostSibling = leftHead
            # And also share their father
            node.father = leftHead.father

        # Return a reference to the right-most sibling
        # print("makeSiblings is returning self (%s)'s the rightMostSibling: %s" % (self, self.getRightMostSibling()))
        # print("New Sibling chain: %s" % leftHead.prettySiblings())
        return self

    def getSiblings(self):
        '''Generator that allows iteration across ALL the siblings from left to right'''
        # Start with the left side of the list
        seek = self.leftmostSibling

        while seek is not None:
            yield seek
            seek = seek.rightSibling

    def getRightMostSibling(self):
        '''Traverses the sibling list to the right (starting at this node) until the last sibling is found'''
        if self.rightSibling is self:
            print("The node %s's right sibling is itself. This is BAD" % self)
            exit(-1)

        # Start at this node
        # print("Starting with %s" % self.rightSibling)
        if self.rightSibling is None:
            return self
        else:
            return self.rightSibling.getRightMostSibling()
            # seek = self.rightSibling

        # # Move right until there isn't a rightSibling
        # while seek.rightSibling is not None:
        #     print("%s -> %s" % (seek, seek.rightSibling))
        #     seek = seek.rightSibling
        # if seek is None:
        #     print("Seek is None! Ah!")
        # return seek

    def adoptChildren(self, y):
        '''
        Makes y and its siblings children of this node.
        Returns a reference to self for easy chaining
        '''
        # Just in case we get nothing. Mostly a precaution against the makeFamily function
        if y is None:
            return self

        if self.leftmostChild is not None:
            # If there are already some children, join their lists
            leftmostChild.makeSiblings(y)
        else:
            # No childen exist yet. Y and its siblings will now be the children
            childHead = y.leftmostSibling

            # You are my children now
            self.leftmostChild = childHead

            # Who's your daddy?
            for luke in childHead.getSiblings():
                luke.father = self
        return self

    def associateSiblings(self, *kids):
        '''
        Recurse through making all the passed in kids my siblings
        Must return the leftSibling
        '''
        if len(kids) == 0:
            return self
        else:
            # Make the next child my sibling, then continue on down the line
            # print("Adding to %s : siblings %s" % (self, kids))
            should_be_self = self.makeSiblings(kids[0])
            # print("After the first kid: %s" % should_be_self)
            return should_be_self.associateSiblings(*kids[1:])

    # def __str__(self):
    #     return str(self.data)

    def __repr__(self):
        return "<%s %s>" % (id(self), self.data)

    def prettySiblings(self):
        if self.rightSibling is not None:
            return self.__repr__() + " : " + self.rightSibling.prettySiblings()
        else:
            return self.__repr__()

    def prettyPrintStructure(self):
        '''Prints the node itself, all its siblings, and all its children'''
        # print(self.prettySiblings())

        # Show yourself
        print(self.__repr__())

        # Who are my children?
        if self.leftmostChild is not None:
            # print(repr(self) + " has at least one child: " + repr(self.leftmostChild) + " : " + repr(self.leftmostChild.rightSibling))
            for child in self.leftmostChild.getSiblings():
                # print("Child: " + repr(child))
                print(repr(self) + " -> " + repr(child))
                child.prettyPrintStructure()
            # print("End of children")

        # for sib in self.getSiblings():
        #     if (sib is not self.leftmostChild
        #         and sib.leftmostChild is not None):
        #         print(sib.__repr__() + " -> " + sib.leftmostChild.__repr__())
        #         sib.leftmostChild.prettyPrintStructure()

        # if self.leftmostChild is not None:
        #     self.leftmostChild.prettyPrintStructure()

    def accept(self, visitor):
        # Visit all my children if I have any
        if self.leftmostChild is not None:
            for child in self.leftmostChild.getSiblings():
                visitor.visit(child)

def makeNode(op):
    '''
    Based on the type of op, make a specific node type.
    '''
    return Node(None, op)

def makeFamily(op, *kids):
    # It's a bit important that if no kids are passed in, then adoptChildren just won't do anything
    # print("Making family with op %s and kid[0] %s" % (op, kids[0]))
    # print("kids with children: %s" % kids[0].associateSiblings(*kids[1:]))
    newFam = makeNode(op).adoptChildren(kids[0].associateSiblings(*kids[1:]))
    # print("New Family:")
    # newFam.prettyPrintStructure()
    # print("")
    return newFam


# Keith made this sound necesary. The book seems to disagree
# class DataNode:
#     def __init__(self, data=None, father=None, leftmostSibling=None, nextSibling=None):
#         self.data = data
#         self.father = father
#         self.leftmostSibling = leftmostSibling
#         self.nextSibling = nextSibling

class Visitor:
    def visit(self, node):
        node.accept(self)

class PrintVisitor(Visitor):
    def __init__(self):
        self.idcount = 0

    def prettyChildren(self, node):
        return "%s" % (id(node))

    def visit(self, node):
        print("%s\t%s\t%s" % (id(node), node.kind, node.data))

        if node.leftmostChild is not None:
            print(id(node), end=" ")
            for child in node.leftmostChild.getSiblings():
                print(id(child), end=" ")
            print()

        self.idcount+=1
        # print(type(super()))
        super().visit(node)
