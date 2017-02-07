# -*- coding: utf-8 -*-
import random
import math

class Solver_8_queens:
    desk_size = 8
    point_size = 3 # num of row in binary
    ppltn_indexes = list() # temp polulation
    ppltn = list()      # current population
    p_size = 0          # ppltn size
    cross_p = 0.5       # corssingover probability
    mutation_p = 0.05   # mutation probability
    max_clashes =  28   
    def __init__(self, pop_size=500, cross_prob=0.7, mut_prob=0.1, desk_size=8):
        self.p_size = pop_size
        self.cross_p = cross_prob
        self.mutation_p = mut_prob
        self.desk_size = desk_size
        self.point_size = int(math.log2(desk_size))
        self.max_clashes =  sum(range(desk_size))

    def solve(self, min_fitness=0.9, max_epochs=100):
        best_fit=None
        epoch_num=None
        visualization=None

        self.generate_ppltn()

        i = 0
        while i < max_epochs and max(self.get_ppltn_fitness(self.ppltn)) < min_fitness:
            self.step_one()
            i = i + 1 
        best_fit = max(self.get_ppltn_fitness(self.ppltn))
        epoch_num = i
        for cell in self.ppltn:
            if self.fitness(cell) == best_fit:
                visualization = self.to_str(cell)
                break
        return best_fit, epoch_num, visualization

    def cell_to_points(self, cell):
        points = list()
        for i in range(self.desk_size):
            cell_part = cell[i * self.point_size:(i + 1) * self.point_size]
            points.append((i, int(''.join(cell_part), 2)))
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
        d = self.max_clashes - self.all_clashes(self.cell_to_points(cell))
        return d / self.max_clashes
   
    def to_str(self, cell):
        res = list(('+' * self.desk_size + '\n') * self.desk_size)
        for p in self.cell_to_points(cell):
            res[p[0] * (self.desk_size + 1)+  p[1]] = 'Q'
        return ''.join(res)
    
    def generate(self):
        cell = list()
        fmt_str = '{0:0' + str(self.point_size) + 'b}'
        for i in range(self.desk_size):
            cell = cell + list(fmt_str.format(random.randrange(self.desk_size)))
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
        return [a[0:k] + b[k: len(a)], b[0: k] + a[k: len(a)]]
            
    def generate_ppltn(self):
        '''generate start population'''
        self.ppltn = list()
        for i in range(self.p_size):
            self.ppltn.append(self.generate())

    def apply_mutation(self, cell):
        try:
            bit_count = random.randrange(int(len(cell) * self.mutation_p))
            for k in random.sample(range(len(cell)), bit_count):
                cell[k] = '1' if cell[k] == '0' else '0'
        except:
            pass
        return cell

    def selection_step(self):
        self.ppltn_indexes = list()        
        probs = self.get_ppltn_probs(self.ppltn);
        for i in range(int(self.p_size * self.cross_p)):
            a = self.ring_select(probs, random.random())
            self.ppltn_indexes.append(a)
           
    
    def crossing_step(self):
        new_ppltn = list()   

        for i in range(self.p_size):
            a = random.randrange(len(self.ppltn_indexes))
            a = self.ppltn_indexes[a]
            b = random.randrange(len(self.ppltn_indexes))
            b = self.ppltn_indexes[b]
            while a == b:
                b = random.randrange(len(self.ppltn_indexes))
                b = self.ppltn_indexes[b]            
            offsprings = self.one_point_crossing(self.ppltn[a], self.ppltn[b])
            new_ppltn = new_ppltn + offsprings
        self.ppltn = new_ppltn

    def mutation_step(self):
        mutation_ppltn = list()
        for cell in self.ppltn:
            cell = self.apply_mutation(cell)
            mutation_ppltn.append(cell)
        self.ppltn = mutation_ppltn

    def step_one(self):
        self.selection_step()
        self.crossing_step()
        self.mutation_step()