import random
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import math

from multiprocessing import Pool
from functools import partial

import os

DEFAULT_LEFT_BORDER = 1
DEFAULT_RIGHT_BORDER = 30

DEFAULT_POLINOM = lambda x: x**3

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

def mutation(individual: Individual, l, r, alpha) -> None:
  temp = individual.getValue()
  value = temp + random.uniform(-2*alpha, 2*alpha)
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

    self.strange_dots = []

  def fitnessFunc(self, individual: Individual) -> float:
    value = self.function(individual.getValue())
    fine = 0.0
    for maximum in self.history_max + self.strange_dots:
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
    temp_y = []
    for i in range(len(self.population)):
      try:
        start_value = self.function(self.population[i].getValue())
      except Exception:
        self.population[i].value = self.population[i].value + 0.001
        start_value = self.function(self.population[i].getValue())
      temp_y.append(start_value)
    
    self.history_y.append(temp_y)
    
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
          mutation(self.population[j], self.left_border, self.right_border, self.alpha)

      self.history_x.append([ind.getValue() for ind in self.population])
      self.history_y.append([self.function(ind.getValue()) for ind in self.population])

      i += 1

    local_ans = [(self.population[i].getValue(), self.function(self.population[i].getValue())) for i in range(self.population_size)]
    found_max = max(local_ans, key=lambda x: x[1])
    found_local_max = self.findLocalMax(local_ans)

    total_ans = None
    if found_local_max != None and found_max[1] == found_local_max[1] or (found_local_max == None and (found_max[0] - self.left_border < 1e-2 or self.right_border - found_max[0] < 1e-2)):
      flag = True
      for maximum in self.history_max:
        if math.fabs(maximum[0] - found_max[0]) < self.sigma_share:
          flag = False
          break
      if flag:
        total_ans = found_max
        self.history_max.append(found_max)

    if total_ans == None:
      self.strange_dots.append(found_max)

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

def save_plots(i, j, max_epochs, l, r, x_func, y_func, history_x, history_y, history_max, population_size, ans, max_iterations, all_history_y):
    plt.figure(figsize=(10, 6))
    plt.plot(x_func, y_func, 'b')
    plt.xlim(l - abs(0.3 * r), r + abs(0.3 * r))
    plt.plot(history_x[i], history_y[i], 'ro')
    plt.grid()

    x_max, y_max = [history_max[i][0] for i in range(len(history_max) - 1)], [history_max[i][1] for i in range(len(history_max) - 1)]
    if ans == None or (j+1)*(i+1) == max_iterations*max_epochs:
      x_max.append(history_max[len(history_max) - 1][0])
      y_max.append(history_max[len(history_max) - 1][1])
    plt.plot(x_max, y_max, 'go')
    plt.xlabel('x')
    plt.ylabel('f(x)')

    plt.title(f"Iteration: {j + 1}, Epoch: {i + 1}")
    filename = f'./frames/algorithm_{j * max_epochs + i}.jpg'
    plt.savefig(filename, dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    average_fitness = [sum(all_history_y[k]) / population_size for k in range(j*(max_epochs + 1) + i + 1)]
    maximum_fitness = [max(all_history_y[k]) for k in range(j*(max_epochs + 1) + i + 1)]
    plt.plot(average_fitness, marker='o', linestyle='-', color='black', markerfacecolor='red', label='Average fitness')
    plt.plot(maximum_fitness, marker='o', linestyle='-', color='blue', markerfacecolor='green', label='Max fitness')
    plt.legend(loc='lower right')
    plt.grid()
    plt.title(f"Iteration: {j + 1}, Epoch: {i + 1}")
    plt.savefig(f'./frames/average_fitness_{j * max_epochs + i}.jpg', dpi=300)
    plt.close()

def run(iterations=ITERATIONS, max_epochs=MAX_EPOCHS,
        l=DEFAULT_LEFT_BORDER, r=DEFAULT_RIGHT_BORDER,
        polinom=DEFAULT_POLINOM, population_size=POPULATION_SIZE,
        p_crossover=P_CROSSOVER, p_mutation=P_MUTATION,
        tournment_opponents=DEFAULT_TOURNMENT_OPPONENTS, alpha=DEFAULT_ALPHA,
        sigma_share=None, visualize=True):
    if sigma_share is None:
      sigma_share = (r - l) / 12 + 1

    if not os.path.exists('frames'):
      os.makedirs('frames')
    else:
      for file in os.listdir('frames'):
        if file.endswith('.jpg'):
            os.remove(os.path.join('frames', file))

    x_func, y_func = getFunctionDots(1000, l, r, polinom)

    random.seed(42)
    A = GenAlgorithm(max_epochs, population_size, l, r, polinom, p_crossover, p_mutation, tournment_opponents, alpha, sigma_share)

    permanent_history_y = []

    with Pool() as pool:
      for j in range(iterations):
        ans = A.fit()

        if visualize:

          permanent_history_y += A.history_y
          worker = partial(save_plots,
                            j=j,
                            max_epochs=max_epochs,
                            l=l,
                            r=r,
                            x_func=x_func,
                            y_func=y_func,
                            history_x=A.history_x,
                            history_y=A.history_y,
                            history_max=A.history_max,
                            population_size=population_size,
                            ans=ans,
                            max_iterations=iterations,
                            all_history_y = permanent_history_y)

          pool.map(worker, range(max_epochs))

        

        A.history_x = []
        A.history_y = []
        print(ans)

    print("Ans:")
    print(A.history_max)
    print("Strange dots:")
    print(A.strange_dots)

    return A.history_max

if __name__ == "__main__":
    run()