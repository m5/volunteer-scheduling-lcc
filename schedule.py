import random
from collections import defaultdict

class Worker:

    def __init__(self,num,shifts):
        self.num = 0
        self.hours_remaining = 10
        self.prefs = defaultdict(lambda:0)
        self.num_avail = 0
        self.num = num
        self.rand_init(shifts)

    def rand_init(self,shifts):
        num_shifts = random.randint(1,shifts/3)
        shifts_avail = [ random.choice(range(shifts)) for n in range(num_shifts) ]
        for shift in shifts_avail:
            self.prefs[shift] = random.choice(range(1,4))
            self.num_avail += 1
    def __repr__(self):
        return "<worker num=%s shifts=%d remaining=%s>" % (self.num,self.num_avail, self.hours_remaining)



class Shift:
    def __init__(self,num,workers):
        self.num_avail = 0
        self.num = 0
        self.scheduled = None
        self.avail = []
        self.num = num
        for worker in workers:
            if worker.prefs[self.num] > 0:
                self.avail.append(worker)
                self.num_avail += 1
    def __repr__(self):
        if self.scheduled:
            return "<shift num=%s sched=%s pref=%s avail=%d>" % (
                self.num, 
                self.scheduled.num, 
                self.scheduled.prefs[self.num], 
                self.num_avail)
        else:
            return "<shift num=%s unscheduled>" % (self.num)


num_shifts = 50
num_workers = 10
workers = [ Worker(n,50) for n in range(10) ]
shifts = [ Shift(n,workers) for n in range(num_workers) ]
shifts.sort(key=lambda s: s.num_avail)

for shift in shifts:
    for worker in sorted(shift.avail, key=lambda w: -w.prefs[shift.num]):
        if worker.hours_remaining > 0:
            shift.scheduled = worker
            worker.hours_remaining -= 1
            break

shifts.sort(key=lambda s:s.num)
for shift in shifts:
    print shift

for worker in workers:
    print worker
