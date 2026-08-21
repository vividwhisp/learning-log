class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.data = value

def Insert(root, value):
        if root is None:
            return Node(value)
        elif root.data == value:
            return root
        elif root.data > value:
            root.left = Insert(root.left, value)
        else:
            root.right = Insert(root.right, value)
        return root

def search(root, value):
        if root is None:
            print("Element not found",end="\n")
            return
        elif root.data == value:
            print("Element Found",end = "\n")
            return
        elif root.data > value:
            search(root.left, value)
        else:
            search(root.right, value)
        

def inOrder(root):
    if root is not None:
        inOrder(root.left)
        print(root.data, end=" ")
        inOrder(root.right)

def inOrderSuccessor(root):
     root = root.right
     while root is not None and root.left is not None:
          root = root.left
     return root


def delete(root, value):
    if root is None:
         return root
    elif root.data > value:
         root.left = delete(root.left, value)
    elif root.data < value:
         root.right = delete(root.right, value)
    else:
         if root.left is None:
             return root.right
         elif root.right is None:
             return root.left
         else:
             succesor = inOrderSuccessor(root)
             root.data = succesor.data
             root.right = delete(root.right,succesor.data)
    return root






root = Insert(None, 20)
root = Insert(root, 15)
root = Insert(root, 30)
root = Insert(root, 40)
root = Insert(root,12)
root = Insert(root, 18)
root = Insert(root, 25)
root = Insert(root, 50)

inOrder(root)

delete(root, 12)
print("\n")
inOrder(root)
delete(root, 15)
print("\n")
inOrder(root)
delete(root, 30)
print("\n")
inOrder(root)