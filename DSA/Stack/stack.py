class Stack:
    def __init__(self):
        self.s = []

    def length(self):
        return len(self.s)

    def push(self, value):
        self.s.insert(0, value)

    