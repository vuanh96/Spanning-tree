from numpy import random
import decode
import numpy as np


class GeneticAlgoritm(object):
    def __init__(self, genetics):
        self.genetics = genetics
        pass

    def run(self):
        population = self.genetics.initial()
        while True:
            fits_pops = [(self.genetics.fitness(ch), ch) for ch in population]
            if self.genetics.check_stop(fits_pops): break
            population = self.next(fits_pops)
            pass
        return population

    def next(self, fits):
        parents_generator = self.genetics.parents(fits)
        size = len(fits)
        nexts = []
        while len(nexts) < size:
            parents = next(parents_generator)
            cross = random.random() < self.genetics.probability_crossover()
            children = self.genetics.crossover(parents) if cross else parents
            for ch in children:
                mutate = random.random() < self.genetics.probability_mutation()
                nexts.append(self.genetics.mutation(ch) if mutate else ch)
                pass
            pass
        return nexts[0:size]

    pass


class GeneticFunctions(object):
    def __init__(self, target, n,
                 limit=1000, size=1000,
                 prob_crossover=0.8, prob_mutation=0.01):
        self.n = n
        self.target = target  # target o day la ma tran trong so
        self.counter = 0

        self.limit = limit
        self.size = size
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation
        pass

    def probability_crossover(self):
        return self.prob_crossover

    def probability_mutation(self):
        return self.prob_mutation

    def initial(self):
        return [self.random_chromo() for j in range(self.size)]

    def fitness(self, chromosome):
        return decode.fitness(chromosome, self.target)

    def check_stop(self, fits_populations):
        r"""stop run if returns True
        - fits_populations: list of (fitness_value, chromosome)
        """
        self.counter += 1

        best_match = list(sorted(fits_populations))[-1][1]
        fits = [f for f, ch in fits_populations]
        best = min(fits)
        worst = max(fits)
        ave = sum(fits) / len(fits)
        print(
            "[G %3d] score=(%4d, %4d, %4d)" %
            (self.counter, best, ave, worst
             ))

        return self.counter >= self.limit

    def parents(self, fits_populations):
        r"""generator of selected parents
        """
        while True:
            father = self.tournament(fits_populations)
            mother = self.tournament(fits_populations)
            yield (father, mother)
            pass
        pass

    def crossover(self, parents):
        father, mother = parents
        index1 = random.randint(1, self.n - 3)
        index2 = random.randint(1, self.n - 3)
        if index1 > index2: index1, index2 = index2, index1
        child1 = father[:index1] + mother[index1:index2] + father[index2:]
        child2 = mother[:index1] + father[index1:index2] + mother[index2:]
        # for i in range(0,self.n-2):
        #     if self.target[father[i]-1][i+1] > 20:
        #         tg = mother[i]
        #         mother[i] = father[i]
        #         father[i] = tg
        # child1 = father
        # child2 = mother
        return child1, child2

    def mutation(self, chromosome):
        r"""mutate chromosome
        """
        index = random.randint(0, self.n - 3)
        mutated = list(chromosome)
        mutated[index] = random.randint(1, self.n)
        return mutated

    # internals

    def tournament(self, fits_populations):
        alicef, alice = self.select_random(fits_populations)
        bobf, bob = self.select_random(fits_populations)
        return alice if alicef > bobf else bob

    def select_random(self, fits_populations):
        return fits_populations[random.randint(0, len(fits_populations) - 1)]

    def random_chromo(self):
        return [random.randint(1, self.n) for i in range(self.n - 2)]

    pass


if __name__ == "__main__":
    n = 5
    w = np.zeros((n, n))
    for i in range(0, n):
        for j in range(i + 1, n):
            w[i][j] = random.randint(1, 100)
    for i in range(0, n):
        for j in range(0, i + 1):
            w[i][j] = w[j][i]
    print(w)
    GeneticAlgoritm(GeneticFunctions(target=w, n=n, limit=100, size=1000)).run()
