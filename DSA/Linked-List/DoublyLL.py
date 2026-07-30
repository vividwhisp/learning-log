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

    def insertAtBeg(self, value):
        temp = Node(value)
        if(self.head == None):
            self.head = temp
            return
        temp.next = self.head
        self.head.prev = temp
        self.head = temp

    def insertInMiddle(self,value,x):
        t = self.head
        temp = Node(value)
        while(t.next != None):
            if(t.data == x):
                break
            else:
                t = t.next
        temp.next = t.next
        t.next.prev = temp
        t.next = temp
        temp.prev = t
            

    def deleteDLL(self,value):
        if(self.head == None):
            print("Linked List is empty")
            return
        
        t = self.head
        if(t.data == value):
            self.head = t.next
            self.head.prev = None
            return
        
        while(t.next != None):
            if(t.data == value):
                t.prev.next = t.next
                t.next.prev = t.prev
                return
            else:
                t = t.next
        if(t.data == value):
            t.prev.next = None
        

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
obj.insertAtBeg(5)
obj.insertInMiddle(50,20)
obj.deleteDLL(50)
obj.printLL()
