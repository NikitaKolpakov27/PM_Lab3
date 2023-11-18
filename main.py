import math
import random
from Utils import ActivityListSampler, ActivityListDecoder
import json

with open('3.json') as f:
    json_data = json.load(f)

# durations
print(json_data['activities'][0]['modes'][0]['duration'])

# predecessors
print(json_data['activities'][0]['predecessors'])

# renewable_demands
print(json_data['activities'][0]['modes'][0]['renewable_demand'])

# renewable_capacities (resources)
print(json_data['renewable_resources'])

# Число активностей
print("Число активностей: ", len(json_data['activities']))

# Верхняя граница
print(json_data['horizon'])

print("==========================================================")

predecessors = []
durations = []
renewable_demands = []
renewable_capacities = json_data['renewable_resources']
horizon = json_data['horizon']

for i in range(0, len(json_data['activities'])):
    predecessors.append(json_data['activities'][i]['predecessors'])

    for j in range(0, len(json_data['activities'][i]['modes'])):
        durations.append(json_data['activities'][i]['modes'][j]['duration'])
        renewable_demands.append(json_data['activities'][i]['modes'][j]['renewable_demand'])


# print("Predecessors:", predecessors)
# print("Durations:", durations)
# print("Renewable demands:", renewable_demands)

sampler = ActivityListSampler(predecessors)
decoder = ActivityListDecoder()
random_activity_list = sampler.generate()
print("random_activity_list: ", random_activity_list)
start_times = decoder.decode(random_activity_list, durations, predecessors, renewable_demands, renewable_capacities)
print("start_times: ", start_times)


def create_random_schedule():
    schedule = []
    for _ in range(0, len(random_activity_list)):
        schedule.append(random.choice(range(0, horizon)))

    return schedule


def simulated_annealing(A):
    x0 = random.choice(range(0, len(A)))              # Начальный элемент
    T = 1000000000000                                 # Начальная температура
    k = 1                                             # Коэффициент уменьшения

    answers = []
    while T > 0.00001:

        x_new = random.choice(range(0, len(A)))       # Подбор соседей
        delta_f = A[x_new] - A[x0]

        if delta_f <= 0:
            x0 = x_new
            answers.append(A[x0])
            A[x0] = A[x_new]
        else:
            prob = (2.72 ** (-1 * delta_f) / (T * 1.0))
            if prob >= 0.5:
                x0 = x_new
                answers.append(A[x0])
                A[x0] = A[x_new]
            else:
                answers.append(A[x_new])

        T = T / math.log2(k + 1)   # "Охлаждение" температуры
        k += 1

    print("Ответы: ", answers, " длина: ", len(answers))
    return [answers, k]


if __name__ == "__main__":
    random_schedule = create_random_schedule()
    print("Random schedule: ", random_schedule)

    res = simulated_annealing(random_schedule)
    print("Новое расписание (ответ): ", res[0], " Количество итераций: ", res[1])
