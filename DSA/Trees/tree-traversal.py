class Node:
    def __init__(self,value):
        self.left = None
        self.right = None
        self.data = value

def preOrder(root):
    if root is not None:
        print(root.data, end=" ")
        preOrder(root.left)
        preOrder(root.right)

def inOrder(root):
    if root is not None:
        inOrder(root.left)
        print(root.data, end=" ")
        inOrder(root.right)

def postOrder(root):
    if root is not None:
        postOrder(root.left)
        postOrder(root.right)
        print(root.data, end=" ")
            

root = Node(1)
root.left = Node(3)
root.right = Node(5)
root.left.left = Node(2)
root.left.right = Node(4)
root.right.right = Node(8)
preOrder(root)
print("\n")
inOrder(root)
print("\n")
postOrder(root)
