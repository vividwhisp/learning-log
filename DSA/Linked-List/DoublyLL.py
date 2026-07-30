class Node:
    def __init__(self,value=None):
        self.data = value
        self.next = None
        self.prev = None

class DoublyLL:
    def __init__(self):
        self.head = None

    def insertAtEnd(self, value):
        temp = Node(value)
        if(self.head == None):
            self.head = temp
            return
        t = self.head
        while t.next != None:
            t = t.next
        t.next = temp
        temp.prev = t

    def printLL(self):
        t = self.head
        while(t.next != None):
            print(t.data, end=" <--> ")
            t = t.next
        print(t.data)

obj = DoublyLL()
obj.insertAtEnd(10)
obj.insertAtEnd(20)
obj.insertAtEnd(30)
obj.insertAtEnd(40)
obj.printLL()
