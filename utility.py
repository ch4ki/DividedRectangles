import numpy as np

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
    def __len__(self):
        return len(self.queue)
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def put(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()
def basis(i, n):
    return np.identity(n)[:,i]

def peek(stack):
    if stack:
        return stack.queue[-1]
    else:
        return None

def fill(value, n):
    vec = np.empty(n)
    return vec.fill(value)