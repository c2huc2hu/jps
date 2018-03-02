import heapq
import itertools

class FastPriorityQueue():
    '''
    Because I don't need threading, I want a faster queue than queue.PriorityQueue
    Implementation copied from: https://docs.python.org/3.3/library/heapq.html
    '''
    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=0):
        'Add a new task'
        count = next(self.counter)
        entry = [priority, count, task]
        heapq.heappush(self.pq, entry)

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            return task
        raise KeyError('pop from an empty priority queue')

    def empty(self):
        return len(self.pq) == 0
