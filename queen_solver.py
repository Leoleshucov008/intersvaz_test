import random
import math
class queen_solve:
    desk_size = 8
    point_size = 6      # 3 bits for row and 3 bits for col
    cell_size = point_size * desk_size

    ppltn = list()      # current population
    p_size = 0          # ppltn size
    cross_p = 0.5       # corssingover probability
    mutation_p = 0.05   # mutation probability
    mutation_count = 6  #
    def __init__(self, p_size=50, cross_p=0.5, mutation_p=0.05, mutation_count = desk_size):
        self.p_size = p_size
        self.cross_p = cross_p

    def to_point(self, _bin):
        return (int(_bin[0:3], 2), int(_bin[3: 6], 2))
    
    def cell_to_points(self, cell):
        points = list()
        for i in range(self.desk_size):
            points.append(self.to_point(''.join(cell[i * self.point_size: (i + 1) * self.point_size])))
        return points

    def is_clash(self, a, b):
        return  a[0] == b[0] or a[1] == b[1] or abs((a[0]-b[0]) / (a[1]-b[1])) == 1

    def all_clashes(self, points):
        _sum = 0
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                _sum = _sum + int(self.is_clash(points[i], points[j]))
        return _sum
    
    def fitness(self, cell):
        return math.exp(-self.all_clashes(self.cell_to_points(cell)))
   
    def to_str(self, cell):
        res = list('+ + + + + + + +\n' * self.desk_size)
        for p in self.cell_to_points(cell):
            res[p[0]* 16 + 2 * p[1]] = 'Q'
        return ''.join(res)
    
    def generate(self):
        cell = list('0' * self.cell_size)
        for i in range(self.cell_size):
            cell[i] = '1' if random.random() < 0.5 else '0'
        return cell
        
    def get_ppltn_fitness(self, ppltn):
        fitness = list()
        for cell in ppltn:
            fitness.append(self.fitness(cell))
        return fitness

    def get_ppltn_probs(self, ppltn):
        probs = self.get_ppltn_fitness(ppltn)
        # normalize
        sum_p = sum(probs)
        last_p = 0
        for i in range(len(probs)):
            probs[i] = last_p + probs[i] / sum_p
            last_p = probs[i]
        return probs
        
    def ring_select(self, probs, p):
        for i in range(len(probs)):
            if p < probs[i]:
                return i
        return len(probs) - 1
        
    def one_point_crossing(self, a, b):
        k = random.randrange(len(a)) 
        return a[0:k] + b[k: len(a)]
            
    def generate_ppltn(self):
        '''generate start ppltn'''
        self.ppltn = list()
        for i in range(self.p_size):
            self.ppltn.append(self.generate())

    def apply_mutation(self, cell):
        for k in random.sample(range(self.cell_size), self.mutation_count):
            cell[k] = '1' if cell[k] == '0' else '0'
        return cell

    def crossing_step(self):
        new_ppltn = list()
        probs = self.get_ppltn_probs(self.ppltn)
        for i in range(self.p_size):
            a = self.ring_select(probs, random.random())
            b = self.ring_select(probs, random.random())
            while a == b:
                b = self.ring_select(probs, random.random())
            new_ppltn.append(self.one_point_crossing(self.ppltn[a], self.ppltn[b]))
        self.ppltn = self.ppltn + new_ppltn

    def mutation_step(self):
        mutation_ppltn = list()
        for cell in self.ppltn:
            if (random.random() < self.mutation_p):
                cell = self.apply_mutation(cell)
            mutation_ppltn.append(cell)
        self.ppltn = mutation_ppltn
    
    def reduction_step(self):
        fitness = list()
        for cell in self.ppltn:
            fitness.append(self.fitness(cell))
        pairs = list(zip(fitness, self.ppltn))
        pairs.sort(key=lambda x: x[0], reverse=True)
        self.ppltn = list()
        for cell in pairs[0: self.p_size]:
            self.ppltn.append(cell[1])

    def step_one(self):
        self.crossing_step()
        self.mutation_step()
        self.reduction_step()

    def run(self, max_fitness, max_iteration):
        self.generate_ppltn()

        i = 0
        while i < max_iteration and max(self.get_ppltn_fitness(self.ppltn)) < max_fitness:
            print (max(self.get_ppltn_fitness(self.ppltn)))
            self.step_one()
            i = i + 1        
