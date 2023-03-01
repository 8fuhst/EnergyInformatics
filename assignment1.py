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


# Assignment 2
def assignment_2():
    prices = [4,  6,  3,  5,  7,  7,  6,  5,  4,  4,  6,  5,  3,  6,  7,  7,  3, 14, 16, 16,  4,  6,  3,  6]
    # prices = build_price_curve(3, 7, 12, 18)
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
    for v in problem.variables():
        print(v.name + " " + str(v.varValue))
    print(value(problem.objective))
    # TODO: Consider non-shiftables, add their price according to price curve


if __name__ == '__main__':
    assignment_2()