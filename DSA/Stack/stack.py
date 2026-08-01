class Stack:
    def __init__(self):
        self.s = []

    def length(self):
        return len(self.s)

    def push(self, value):
        self.s.insert(0, value)

    def peek(self):
        if len(self.s) == 0:
            raise Exception("Stack is Empty")
        else:
            return self.s[0]

    def pop(self):
        if len(self.s) == 0:
            raise Exception("Stack is Empty")
        else:
            return self.s.pop(0)


obj = Stack()
obj.push(10)
obj.push(20)
obj.push(30)
print(obj.pop())
print(obj.pop())
print(obj.pop())
print(obj.peek())
