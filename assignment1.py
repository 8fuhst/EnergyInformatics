import random
import matplotlib.pyplot as plt
import numpy as np
from pulp import *


def build_price_curve(low_off, high_off, low_on, high_on):
    prices = []
    LOW_PRICE_OFF_PEAK = low_off
    HIGH_PRICE_OFF_PEAK = high_off
    LOW_PRICE_PEAK = low_on
    HIGH_PRICE_PEAK = high_on
    for i in range(0, 24):
        if i < 17 or i >= 20:  # Off-peak hours
            prices.append(random.randint(LOW_PRICE_OFF_PEAK, HIGH_PRICE_OFF_PEAK))
        else:  # On-peak hours
            prices.append(random.randint(LOW_PRICE_PEAK, HIGH_PRICE_PEAK))
    prices = np.array(prices)
    print(prices)
    plt.plot(prices)
    plt.xticks([x for x in range(0, 24)])
    plt.xlabel('Hours')
    plt.ylabel('Prices')
    plt.title('Price Curve')
    plt.show()
    return prices


def create_input(p: LpProblem):
    lst = []
    for v in p.variables():
        if v.varValue != 0:
            lst.append((v.name, v.varValue))
    return lst


def create_usage_plots(lst: list):
    # variables_list = [x[0] for item in items for items in lst]
    for l in lst:
        pass


# Assignment 2
def assignment_2():
    prices = [4,  6,  3,  5,  7,  7,  6,  5,  4,  4,  6,  5,  3,  6,  7,  7,  3, 14, 16, 16,  4,  6,  3,  6]
    problem = LpProblem('Demand Response', LpMinimize)
    hours = [x for x in range(0, 24)]
    d = LpVariable.dict('Dishwasher', hours, lowBound=0, cat=LpInteger)
    l = LpVariable.dict('Laundry machine', hours, lowBound=0, cat=LpInteger)
    c = LpVariable.dict('Clothes dryer', hours, lowBound=0, cat=LpInteger)
    e = LpVariable.dict('Electric vehicle', hours, lowBound=0, cat=LpInteger)
    v = LpVariable.dict('Vacuum', hours, lowBound=0, cat=LpInteger)
    h = LpVariable.dict('Hair Dryer', hours, lowBound=0, cat=LpInteger)
    m = LpVariable.dict('Microwave', hours, lowBound=0, cat=LpInteger)

    # Objective function
    problem += lpSum([prices[i]*(d[i] + l[i] + c[i] + e[i] + v[i] + h[i] + m[i]) for i in hours]), 'Objective Function'

    # Constraints
    problem.addConstraint(lpSum(d[i] for i in hours) == 1.44), 'Dishwasher Constraint'
    problem.addConstraint(lpSum(l[i] for i in hours) == 1.94), 'Laundry Machine Constraint'
    problem.addConstraint(lpSum(c[i] for i in hours) == 2.5), 'Clothes Dryer Constraint'
    problem.addConstraint(lpSum(e[i] for i in hours) == 9.9), 'Electric Vehicle Constraint'
    problem.addConstraint(lpSum(v[i] for i in hours) == 0.23), 'Vacuum Constraint'
    problem.addConstraint(lpSum(h[i] for i in hours) == 0.25), 'Hair Dryer Constraint'
    problem.addConstraint(lpSum(m[i] for i in hours) == 0.6), 'Microwave Constraint'

    problem.solve()
    print(create_input(problem))
    """for v in problem.variables():
        print(v.name + " " + str(v.varValue))
    print(value(problem.objective))"""
    # TODO: Consider non-shiftables, add their price according to price curve


def assignment_3():
    prices = [4,  6,  3,  5,  7,  7,  6,  5,  4,  4,  6,  5,  3,  6,  7,  7,  3, 14, 16, 16,  4,  6,  3,  6]
    hours = [x for x in range(0, 24)]
    total = 0
    EV_CHANCE = 0.66  # Assume that 2/3rds of households have EV
    output_dict = {}
    input_list = []
    random_appliances_dict = {'Vacuum': 0.23,
                              'Hair Dryer': 0.25,
                              'Microwave': 0.6,
                              'Phone Charger': 0.005,
                              'Ceiling Fan': 0.075}
    for i in range(0, 30):
        appliances_list = []
        device_1 = random.choice(list(random_appliances_dict.items()))
        device_2 = random.choice(list(random_appliances_dict.items()))
        while device_1 == device_2:
            device_2 = random.choice(list(random_appliances_dict.items()))
        device_3 = random.choice(list(random_appliances_dict.items()))
        while device_1 == device_3 or device_2 == device_3:
            device_3 = random.choice(list(random_appliances_dict.items()))
        appliances_list.append(device_1[0])
        appliances_list.append(device_2[0])
        appliances_list.append(device_3[0])

        problem = LpProblem('Demand Response', LpMinimize)
        d = LpVariable.dict('Dishwasher', hours, lowBound=0, cat=LpInteger)
        l = LpVariable.dict('Laundry machine', hours, lowBound=0, cat=LpInteger)
        c = LpVariable.dict('Clothes dryer', hours, lowBound=0, cat=LpInteger)
        e = LpVariable.dict('Electric vehicle', hours, lowBound=0, cat=LpInteger)
        d1 = LpVariable.dict(device_1[0], hours, lowBound=0, cat=LpInteger) # device 1
        d2 = LpVariable.dict(device_2[0], hours, lowBound=0, cat=LpInteger) # device 2
        d3 = LpVariable.dict(device_3[0], hours, lowBound=0, cat=LpInteger) # device 3

        # Objective function
        problem += lpSum([prices[i]*(d[i] + l[i] + c[i] + e[i] + d1[i] + d2[i] + d3[i]) for i in hours]), 'Objective Function'

        # Constraints
        problem.addConstraint(lpSum(d[i] for i in hours) == 1.44), 'Dishwasher Constraint'
        problem.addConstraint(lpSum(l[i] for i in hours) == 1.94), 'Laundry Machine Constraint'
        problem.addConstraint(lpSum(c[i] for i in hours) == 2.5), 'Clothes Dryer Constraint'
        if random.random() <= EV_CHANCE:  # Only add if Household has EV
            problem.addConstraint(lpSum(e[i] for i in hours) == 9.9), 'Electric Vehicle Constraint'
            appliances_list.append('EV')
        problem.addConstraint(lpSum(d1[i] for i in hours) == d1[1]), 'Device 1 Constraint'
        problem.addConstraint(lpSum(d2[i] for i in hours) == d2[1]), 'Device 2 Constraint'
        problem.addConstraint(lpSum(d3[i] for i in hours) == d3[1]), 'Device 3 Constraint'

        problem.solve()
        total += value(problem.objective)
        output_dict[f"Household {i}"] = appliances_list
        input_list.append(create_input(problem))
        """for v in problem.variables():
            print(v.name + " " + str(v.varValue))
        print(value(problem.objective))"""

    values = output_dict.values()
    amount_evs = sum('EV' in item for item in values)
    # print(output_dict)
    print(input_list)
    print(f"Amount of EVs: {amount_evs}")
    print(f"Share of electric vehicles: {amount_evs/30}")
    print(f"Total price of all households for the day: {total}")  # Total price of all households over the day
    # TODO: Consider non-shiftables, add their price according to price curve
    # Since we don't have to consider grid load, every household can use the same appliances at the same time
    # to save money (everyone uses the optimal solution).


def assignment_4():
    prices = [4, 6, 3, 5, 7, 7, 6, 5, 4, 4, 6, 5, 3, 6, 7, 7, 3, 14, 16, 16, 4, 6, 3, 6]
    problem = LpProblem('Demand Response', LpMinimize)
    hours = [x for x in range(0, 24)]
    L = 9
    d = LpVariable.dict('Dishwasher', hours, lowBound=0, cat=LpInteger)
    l = LpVariable.dict('Laundry machine', hours, lowBound=0, cat=LpInteger)
    c = LpVariable.dict('Clothes dryer', hours, lowBound=0, cat=LpInteger)
    e = LpVariable.dict('Electric vehicle', hours, lowBound=0, cat=LpInteger)
    v = LpVariable.dict('Vacuum', hours, lowBound=0, cat=LpInteger)
    h = LpVariable.dict('Hair Dryer', hours, lowBound=0, cat=LpInteger)
    m = LpVariable.dict('Microwave', hours, lowBound=0, cat=LpInteger)

    # Objective function
    problem += lpSum(
        [prices[i] * (d[i] + l[i] + c[i] + e[i] + v[i] + h[i] + m[i])
         + lpSum(d[i] + l[i] + c[i] + e[i] + v[i] + h[i] + m[i]) for i in hours]), 'Objective Function'

    # Constraints
    problem.addConstraint(lpSum(d[i] for i in hours) == 1.44), 'Dishwasher Constraint'
    problem.addConstraint(lpSum(l[i] for i in hours) == 1.94), 'Laundry Machine Constraint'
    problem.addConstraint(lpSum(c[i] for i in hours) == 2.5), 'Clothes Dryer Constraint'
    problem.addConstraint(lpSum(e[i] for i in hours) == 9.9), 'Electric Vehicle Constraint'
    problem.addConstraint(lpSum(v[i] for i in hours) == 0.23), 'Vacuum Constraint'
    problem.addConstraint(lpSum(h[i] for i in hours) == 0.25), 'Hair Dryer Constraint'
    problem.addConstraint(lpSum(m[i] for i in hours) == 0.6), 'Microwave Constraint'
    for i in hours:
        problem.addConstraint(d[i] + l[i] + c[i] + e[i] + v[i] + h[i] + m[i] <= L), 'Maximum Load Constraint'

    problem.solve()
    for v in problem.variables():
        print(v.name + " " + str(v.varValue))
    print(value(problem.objective))
    # TODO: Consider non-shiftables, add their price according to price curve
    # TODO: Maybe add normalization for objective function


if __name__ == '__main__':
    assignment_3()