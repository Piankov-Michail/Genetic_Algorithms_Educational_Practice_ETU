import random
import matplotlib.pyplot as plt
import math

import os
import imageio
import shutil

DEFAULT_LEFT_BORDER = -30
DEFAULT_RIGHT_BORDER = 30

DEFAULT_POLINOM = lambda x: -1*(143771*x)/120120 - (462029*x**2)/2402400 + (1371593*x**3)/72072000 + (35177*x**4)/48048000 - (31949*x**5)/655200000 - (3539*x**6)/6006000000 + (809*x**7)/25740000000

POPULATION_SIZE = 15
P_CROSSOVER = 0.7
P_MUTATION = 0.1
MAX_EPOCHS = 15
ITERATIONS = 5

DEFAULT_TOURNMENT_OPPONENTS = 3
DEFAULT_ALPHA = 1

class Individual:
  def __init__(self, x: float) -> None:
    self.value = x
  def getValue(self) -> float:
    return self.value
  def __repr__(self) -> str:
    return str(self.value)

def createIndividual(x: float) -> Individual:
  return Individual(x)

def createPopulation(n: int, l: float, r: float):
    population= []

    interval_length = r - l
    step = interval_length / n
    current = l
    while(current < r):
      population.append(createIndividual(current))
      current += step
    return population

def mutation(individual: Individual, l, r) -> None:
  temp = individual.getValue()
  value = temp + random.uniform(-2, 2)
  value = max(min(value, r), l)
  individual.value = value

def crossFunc(first: Individual, second: Individual, alpha, l, r) -> Individual:
  x = first.getValue()
  if random.random() < 0.5:
    x = second.getValue()
  left_border = x - alpha
  right_border = x + alpha

  child_value = random.uniform(left_border, right_border)

  child_value = max(min(child_value, r), l)

  return Individual(child_value)

class GenAlgorithm:
  def __init__(self, max_epochs=MAX_EPOCHS, population_size=POPULATION_SIZE,\
               left_border=DEFAULT_LEFT_BORDER, right_border=DEFAULT_RIGHT_BORDER,\
               function=DEFAULT_POLINOM, p_crossover=P_CROSSOVER,\
               p_mutation=P_MUTATION, tournment_opponents=DEFAULT_TOURNMENT_OPPONENTS,\
               alpha=DEFAULT_ALPHA, sigma_share=1) -> None:
    self.population_size = population_size
    self.p_crossover = p_crossover
    self.p_mutation = p_mutation
    self.max_epochs = max_epochs
    self.sigma_share = sigma_share
    self.alpha = alpha
    self.tournment_opponents = tournment_opponents

    self.function = function
    self.left_border = left_border
    self.right_border = right_border

    self.history_x = []
    self.history_y = []
    self.history_max = []
    self.population = None

  def fitnessFunc(self, individual: Individual) -> float:
    value = self.function(individual.getValue())
    fine = 0.0
    for maximum in self.history_max:
      if math.fabs(maximum[0] - individual.getValue()) < self.sigma_share:
        fine += (self.right_border - self.left_border)*2 / (math.fabs(maximum[0] - individual.getValue()) + 0.001)

    return value - fine

  def tournmentSelection(self, population):
    selected = []
    for _ in range(self.population_size):
      participants = random.sample(population, self.tournment_opponents)
      best_ind = max(participants, key=lambda ind: self.fitnessFunc(ind))
      selected.append(best_ind)
    return selected

  def findLocalMax(self, ans):
    result = None
    ans = sorted(ans, key=lambda x: x[0])
    for i in range(1, len(ans) - 1):
      if ans[i-1][1] < ans[i][1] > ans[i+1][1]:
        result = ans[i]
    return result


  def fit(self):
    self.population = createPopulation(self.population_size, self.left_border, self.right_border)

    self.history_x.append([ind.getValue() for ind in self.population])
    self.history_y.append([self.function(ind.getValue()) for ind in self.population])

    state = []
    i = 0
    while(i < self.max_epochs):

      best_ind = self.tournmentSelection(self.population)
      best_ind_shuffled = self.tournmentSelection(self.population)
      random.shuffle(best_ind_shuffled)

      childs = []
      for j in range(self.population_size):
        if random.random() < self.p_crossover:
          childs.append(crossFunc(best_ind[j], best_ind_shuffled[j], self.alpha, self.left_border, self.right_border))

      childs_length = len(childs)
      add = set()
      while(childs_length) < self.population_size:
        choise = random.choice(self.population)

        if not(choise in add):
          add.add(choise)
          childs_length += 1

      self.population = childs + list(add)

      for j in range(self.population_size):
        if random.random() < self.p_mutation:
          mutation(self.population[j], self.left_border, self.right_border)

      self.history_x.append([ind.getValue() for ind in self.population])
      self.history_y.append([self.function(ind.getValue()) for ind in self.population])

      i += 1

    local_ans = [(self.population[i].getValue(), self.function(self.population[i].getValue())) for i in range(self.population_size)]
    found_max = max(local_ans, key=lambda x: x[1])
    found_local_max = self.findLocalMax(local_ans)

    total_ans = None
    if found_local_max != None and found_max[1] == found_local_max[1]:
      total_ans = found_max
      self.history_max.append(found_max)

    return total_ans

def getFunctionDots(n: int, l: float, r: float, func):
    interval_length = r - l
    step = interval_length / n
    current = l
    x = []
    y = []
    while(current < r):
      x.append(current)
      y.append(func(current))
      current += step
    return x, y

def run(iterations=ITERATIONS, max_epochs=MAX_EPOCHS,\
        l=DEFAULT_LEFT_BORDER, r=DEFAULT_RIGHT_BORDER,\
        polinom=DEFAULT_POLINOM, population_size=POPULATION_SIZE,\
        p_crossover=P_CROSSOVER, p_mutation=P_MUTATION,
        tournment_opponents=DEFAULT_TOURNMENT_OPPONENTS, alpha=DEFAULT_ALPHA):
  sigma_share = (r - l)/12 + 1

  if not os.path.exists('frames'):
    os.makedirs('frames')
  else:
    for file in os.listdir('frames'):
      if file.endswith('.png'):
        os.remove(os.path.join('frames', file))

  random.seed(42)
  A = GenAlgorithm(max_epochs, population_size, l, r, polinom, p_crossover, p_mutation, tournment_opponents, alpha, sigma_share)

  for j in range(ITERATIONS):
    ans = A.fit()

    os.makedirs(f'./frames_{j}', exist_ok=True)
    for i in range(max_epochs):
      x, y = getFunctionDots(1000, l, r, polinom)
      plt.plot(x, y, 'b')
      plt.xlim(l - abs(0.3*r), r+abs(0.3*r))
      plt.plot(A.history_x[i], A.history_y[i], 'ro')

      filename = f'./frames_{j}/frame_{i}.png'
      plt.savefig(filename)
      plt.close()

    filenames = sorted([f'./frames_{j}/frame_{i}.png' for i in range(max_epochs)],
                      key=lambda x: int(x.split('_')[-1].split('.')[0]))
    images = [imageio.imread(filename) for filename in filenames]
    imageio.mimsave(f'./animation_{j}.gif', images, fps=1)
    A.history_x = []
    A.history_y = []

    shutil.rmtree(f'./frames_{j}')
    print(ans)

  print(A.history_max)

  shutil.rmtree(f'./frames')

if __name__ == "__main__":
  run()