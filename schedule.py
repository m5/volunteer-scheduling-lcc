import random
import copy
from collections import defaultdict

class Worker(object):
    def __init__(self,num=0,shifts=0,rand=True):
        self.prefs = defaultdict(lambda:0)
        self.num_avail = 0
        self.num = num
        if rand:
            self.rand_init(shifts)
        self.name = ''
        self.num_shifts = 0

    def rand_init(self,shifts):
        self.min_shifts = random.choice(range(6))
        self.max_shifts = random.choice(range(self.min_shifts,20))
        self.preferred_shifts = random.choice(range(self.min_shifts,self.max_shifts+1))
        self.shifts_remaining = self.max_shifts
        num_shifts = random.randint(1,shifts/3)
        shifts_avail = [ random.choice(range(shifts)) for n in range(num_shifts) ]
        for shift in shifts_avail:
            self.prefs[shift] = random.choice(range(1,4))
            self.num_avail += 1
        
    def __repr__(self):
        return "<worker num=%s shifts=%d preferred=%s min=%s max=%s>" % (
            self.num,
            self.num_shifts,
            self.preferred_shifts,
            self.min_shifts,
            self.max_shifts
            )



class Shift(object):
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
            return "<shift num=%s num_avail=%s unscheduled>" % (self.num, self.num_avail)

def assign_shifts(shifts):
    """
     The algorithm assigns the unassigned shift 
     with the least availability 
     to the worker who wants it the most.
     """
    shifts.sort(key=lambda s: s.num_avail)
    for shift in shifts:
        for worker in sorted(shift.avail, key=lambda w: -w.prefs[shift.num]):
            if worker.shifts_remaining > 0:
                shift.scheduled = worker
                worker.shifts_remaining -= 1
                worker.num_shifts += 1
                break
            
def assess_fitness(shifts, workers):
    shift_covered_weight = 20
    under_min_penalty = 5
    over_max_penalty = 5
    near_preferred_weight = 3
    shift_preference_weight = 2
    fitness = 0
    for shift in shifts:
        if shift.scheduled:
            fitness += shift_covered_weight
            fitness += shift.scheduled.prefs[shift.num] * shift_preference_weight
    for worker in workers:
        if worker.num_shifts < worker.min_shifts:
            fitness -= (worker.min_shifts - worker.num_shifts) * under_min_penalty
        if worker.num_shifts > worker.max_shifts:
            fitness -= (worker.num_shifts - worker.max_shifts) * over_max_penalty
        fitness -= near_preferred_weight * abs(worker.num_shifts - worker.preferred_shifts)
    return fitness

class Mutator(object):
    def __init__(self, shifts, workers):
        self.shifts = shifts
        self.workers = workers
        self.mutations = []

    def mutate(self):
        s = random.choice(self.shifts)
        if s.scheduled:
            s.scheduled.num_shifts -= 1
        if s.avail:
            w = random.choice(s.avail)
            p = s.scheduled
            s.scheduled = w
            s.scheduled.num_shifts += 1
            self.mutations.append( (s, p, w) )
    def revert(self):
        (s, p, w) = self.mutations.pop()
        if s:
            s.scheduled = p
        if p:
            p.num_shifts += 1
        if w:
            w.num_shifts -= 1

def climb_hill(shifts, workers):
    fitness = assess_fitness(shifts,workers)
    best_fitness = fitness
    mutations_since_benifit = 0
    m = Mutator(shifts, workers)
        
    while mutations_since_benifit < 50:
        m.mutate()
        fitness = assess_fitness(shifts,workers)
        print fitness, best_fitness
        if fitness > best_fitness:
            mutations_since_benifit = 0
            best_fitness = fitness
        if fitness == best_fitness:
            mutations_since_benifit += 1
        if fitness < best_fitness:
            m.revert()
            mutations_since_benifit += 1

    
    


# Building some random data
num_shifts = 30*5
num_workers = 30
workers = [ Worker(n,num_shifts) for n in range(num_workers) ]
shifts = [ Shift(n,workers) for n in range(num_shifts) ]
assign_shifts(shifts)
climb_hill(shifts,workers)

shifts.sort(key=lambda s:s.num)
for shift in shifts:
    print shift

for worker in workers:
    print worker
