import numpy as np
from random import choice
from itertools import permutations
from bdsolve.game.board import Board
from bdsolve.game.pieces import get_occupation, get_random3

class GA:

    def __init__(self, pop_count=100):
        self.pop_count = pop_count
        self.crossover_rate = 0.25
        self.mutation_rate = 0.4

        self.population = np.zeros((pop_count, 8))
        self.pop_score = np.zeros(pop_count)
        self.pop_success_rate_s = np.zeros(pop_count)
        self.pop_success_rate_c = np.zeros(pop_count)
        self.total_success_rate = [0, 0, 0]

        self.gen_num = 0
        self.pop_num = 0
        self.new_population()

    def new_population(self):
        '''
        Create a population with random genomes.
        '''
        for i in range(self.pop_count):
            self.population[i] = self.get_random_gene(np.zeros(8))
        self.total_success_rate = [0, 0, 0]
        self.pop_success_rate_s *= 0
        self.pop_success_rate_c *= 0
        self.pop_score *= 0
        self.pop_num = 0

    def new_child(self, g1, g2, mutate=True):
        '''
        Create a child genome from two parents.
        Perform crossover and mutation of single genes.

        TODO: n parents, crossover rules, more mutation methods
              (random offset, multiple genes, ...)
        '''
        g = np.zeros(8)
        mut_i = (np.random.choice(np.arange(0, 8))
        if abs(np.random.random()) < self.mutation_rate
        else -1)
        for i in range(8):
            if mutate and i == mut_i:
                gene = float(self.get_random_gene(0))
            else:
                if abs(np.random.random()) < 0.5:
                    gene = g1[i]
                else:
                    gene = g2[i]
            g[i] = gene
        return g

    def new_generation(self):
        '''
        Advance to the next generation.
        Once the fitness of every genome in the population is evaluated,
        perform selection according to current and past performance, then
        replace some part of the population with children of surviving genomes.

        TODO: more selection methods, n parents, different selection criterion,
              variable population size, aging, ...
        '''
        parents, reborn = [], []

        best_genome = np.argmax(self.pop_score)
        worst_genome = np.argmin(self.pop_score)
        fitness = np.vectorize(lambda i: 1-(1/(1+i)))(self.pop_score)
        score_sum = np.sum(self.pop_score)
        fitness_sum = np.sum(fitness)

        print('best: ', best_genome)
        print('worst: ', worst_genome)

        for i, score in enumerate(self.pop_score):
            s = self.pop_success_rate_s[i]
            c = self.pop_success_rate_c[i]
            self.pop_success_rate_s[i] = s*c+(score/self.pop_score[best_genome])/(c+1)
            self.pop_success_rate_c[i] += 1

        b, w, c = self.total_success_rate
        self.total_success_rate[0] = (b*c+self.pop_success_rate_s[best_genome])/(c+1)
        self.total_success_rate[1] = (w*c+self.pop_success_rate_s[worst_genome])/(c+1)
        self.total_success_rate[2] += 1

        for i, score in enumerate(self.pop_score):
            s = self.pop_success_rate_s[i]
            c = self.pop_success_rate_c[i]
            if (abs(np.random.random()) < 0.70
            and (s < self.total_success_rate[1]*1.2
            or i == worst_genome) and c > 3):
                reborn.append(i)
            if (s > self.total_success_rate[1]*1.2
            or i == best_genome):
                parents.append(i)

        print('rip: ', reborn)
        print('par: ', parents)

        if len(reborn) and len(parents) > 1:
            for i in reborn:
                self.population[i] = self.new_child(
                    self.population[choice(parents)],
                    self.population[choice(parents)]
                )
                self.pop_success_rate_s[i] = 0
                self.pop_success_rate_c[i] = 0

        self.gen_num += 1
        self.pop_num = 0
        return score_sum

    @staticmethod
    @np.vectorize
    def get_random_gene(_):
        '''
        Create a random gene (number between -10 and 10).

        TODO: separate genes into their own class
        '''
        return (np.math.floor(abs(np.random.random())*2000)-1000)/100

class Player:

    def __init__(self):
        self.g = GA()
        self.best_rate_genome = None
        self.best_score_genome = None

        self.board = Board()
        self.score = 0
        self.hi_score = 0
        self.avg_score = 0
        self.avg_scores = []

    def evaluate(self, piece, pos, b):
        '''
        View the current genome as a (shallow) neural network.
        Evaluate with properties of board 'b' as its input,
        if piece 'piece' would be at position 'pos'.

        TODO: phenotype from genome (encode full NN), use more layers (deep NN)
        '''
        g = self.g.population[self.g.pop_num]
        b = b.copy()
        b.place(piece, pos)
        return np.sum(g * np.array([
            b.col_integrity,
            b.row_integrity,
            b.block_integrity,
            b.occupation,
            get_occupation(piece),
            1,
            b.subset_occupation,
            0#b.integrity
        ]))

    def play(self):
        '''
        Play a round (3 moves) of the current game with the current genome.
        Try to find the optimal order and positions of the 3 given pieces
        using the current genome to evaluate a possible sequence of decisions.
        Returns the score or False if no more legal moves are possible.

        TODO: optimize for score (Monte Carlo search)
        '''
        opt_val_sum = 0
        opt_order = []
        opt_positions = []
        pieces = get_random3()
        for order in permutations(pieces):
            b = self.board.copy()
            val_sum = 0
            pos_ls = []
            for piece in order:
                y, x = piece.shape
                opt_val = 0
                opt_pos = (0, 0)
                for i in range(1+b.s-y):
                    for j in range(1+b.s-x):
                        if not 2 in (b.board[i:i+y, j:j+x] + piece):
                            val = abs(self.evaluate(piece, (i, j), b))
                            if opt_val > val or not opt_val:
                                opt_val = val
                                opt_pos = (i, j)
                if opt_val:
                    val_sum += opt_val
                    pos_ls.append(opt_pos)
                    b.place(piece, opt_pos)
                    b.reduce_subsets()
                else:
                    break
            if len(pos_ls) == 3:
                if opt_val_sum > val_sum or not opt_val_sum:
                    opt_val_sum = val_sum
                    opt_positions = pos_ls
                    opt_order = order
        if opt_val_sum:
            score = 0
            for piece, pos in zip(opt_order, opt_positions):
                sc = self.board.place(piece, pos)
                ore = self.board.reduce_subsets()
                score += (sc+ore)
            return score
        else:
            return False

    def learn(self):
        '''
        Optimize using the genetic approach.

        TODO: parallel score evaluation, more statistics reporting,
              save to/resume from storage
        '''
        s = self.play()
        if s:
            self.score += s
        else:
            self.g.pop_score[self.g.pop_num] = self.score
            self.score = 0
            self.g.pop_num += 1
            if self.g.pop_num < self.g.pop_count:
                self.board.reset()
            else:
                score_sum = self.g.new_generation()
                self.avg_score = np.round(score_sum / self.g.pop_count, 2)
                self.avg_scores.append(self.avg_score)
                self.best_rate_genome = \
                    self.g.population[np.argmax(self.g.pop_success_rate_s)]
                self.best_score_genome = \
                    self.g.population[np.argmax(self.g.pop_score)]
                self.hi_score = int(np.max(self.g.pop_score))
                self.board.reset()
