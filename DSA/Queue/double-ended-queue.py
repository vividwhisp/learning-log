class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def insertAtEnd(self,value):
        self.items.append(value)

    def deleteAtFront(self):
        if(self.isEmpty()):
            raise Exception("Queue does not Exist")
        else:
            self.items.pop(0)

    def insertAtFront(self,value):
        self.items.insert(0,value)

    def deleteAtEnd(self):
        if(self.isEmpty()):
            raise Exception("Queue does not Exist")
        else:
            return self.items.pop()

dq = Deque()
dq.insertAtEnd(10)
dq.insertAtFront(20)
dq.insertAtEnd(30)
dq.insertAtEnd(40)
dq.insertAtFront(50)
print(dq.deleteAtEnd())
print(dq.deleteAtEnd())
