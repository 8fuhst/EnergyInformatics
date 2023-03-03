import random
import matplotlib.pyplot as plt
import numpy as np
from pulp import *


def build_price_curve(low_off, high_off, low_on, high_on):
    """Only used once in the beginning to build a price curve. Re-run if you wish to create a new curve,
    or call at the beginning of the assignment-methods to automatically use."""
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
    """Used to convert the variable values of an LpProblem into an input list for create_usage_plots_task_3."""
    lst = []
    for v in p.variables():
        if v.varValue != 0:
            lst.append((v.name, v.varValue))
    return lst


def flatten(lst: list):
    return [item for sublist in lst for item in sublist]
"""def create_usage_plots_task_2_4(lst: list):
    hours = [x for x in range(23)]
    data = np.array(lst)
    data = data.flatten()
    print(data)"""

def create_usage_plots_task_2_3(lst: list):
    """Draws a stacked bar chart for the use of household appliances in a neighborhood."""
    variables_list = [[item[0] for item in items] for items in lst]
    flat_list = flatten(variables_list)
    count_dict = {}
    ev = np.zeros(24)
    vacuum = np.zeros(24)
    fan = np.zeros(24)
    dryer = np.zeros(24)
    laundry = np.zeros(24)
    dishwasher = np.zeros(24)
    hairdryer = np.zeros(24)
    microwave = np.zeros(24)
    phone = np.zeros(24)
    for l in flat_list:
        if l not in count_dict.keys():
            count_dict[l] = flat_list.count(l)
    # print(count_dict)
    for k, v in count_dict.items():
        _, k_2 = k.split("_")
        k_2 = int(k_2)
        if 'electric' in k.lower():
            ev[k_2] = v
        elif 'vacuum' in k.lower():
            vacuum[k_2] = v
        elif 'fan' in k.lower():
            fan[k_2] = v
        elif 'dryer' in k.lower():
            dryer[k_2] = v
        elif 'laundry' in k.lower():
            laundry[k_2] = v
        elif 'dish' in k.lower():
            dishwasher[k_2] = v
        elif 'microwave' in k.lower():
            microwave[k_2] = v
        elif 'phone' in k.lower():
            phone[k_2] = v
        elif 'hair' in k.lower():
            hairdryer[k_2] = v
    values = {
        "EV": ev,
        "Vacuum": vacuum,
        "Ceiling Fan": fan,
        "Dryer": dryer,
        "Laundry Machine": laundry,
        "Dishwasher": dishwasher,
        "Microwave": microwave,
        "Phone Charger": phone,
        "Hairdryer": hairdryer
    }
    bottom = np.zeros(24)

    for name, count in values.items():
        plt.bar([x for x in range(24)], count, label=name, bottom=bottom)
        bottom += count

    plt.xticks([x for x in range(24)])
    plt.title("Amount of Appliances used at a Given Time")
    plt.legend(loc="upper right")
    plt.show()


def create_usage_plots_task_4(lst: list, thresh: int):
    data = flatten(lst)
    for i, x in enumerate(data):
        if type(data[i]) is str:
            data[i] = data[i].split('_')[1]
    data = np.array(data)
    data = data.reshape((8, 2))
    sum_list = np.zeros(24)
    print(data.T[0])
    print(data)
    thresh = np.full(24, thresh)
    for e, i in enumerate(data.T[0]):
        print(i)
        sum_list[int(i)] += float(data.T[1][e])
    # print(sum_list)
    plt.bar([x for x in range(24)], sum_list, color="grey", label="Usage in kWh")
    plt.plot([x for x in range(24)], thresh, color="black", label="Max. Capacity")
    plt.xticks([x for x in range(24)])
    plt.legend(loc="upper left")
    plt.title("Usage for a single household when operating under a Threshold")
    plt.show()
    # data = data.T

    # --------------------
    """times = data[0]
    usage = data[1]
    bottom = np.zeros(24)
    

    for time, use in times, usage:
        plt.bar([x for x in range(24)], )
    print(data)"""

# Assignment 2
def assignment_2():
    prices = [4,  6,  3,  5,  7,  7,  6,  5,  4,  4,  6,  5,  3,  6,  7,  7,  3, 14, 16, 16,  4,  6,  3,  6]
    problem = LpProblem('Demand Response', LpMinimize)
    hours = [x for x in range(0, 24)]
    d = LpVariable.dict('Dishwasher', hours, lowBound=0, cat=LpInteger)
    l = LpVariable.dict('LaundryMachine', hours, lowBound=0, cat=LpInteger)
    c = LpVariable.dict('ClothesDryer', hours, lowBound=0, cat=LpInteger)
    e = LpVariable.dict('ElectricVehicle', hours, lowBound=0, cat=LpInteger)
    v = LpVariable.dict('Vacuum', hours, lowBound=0, cat=LpInteger)
    h = LpVariable.dict('HairDryer', hours, lowBound=0, cat=LpInteger)
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
    create_usage_plots_task_2_3([create_input(problem)])
    """for v in problem.variables():
        print(v.name + " " + str(v.varValue))"""
    print(value(problem.objective))
    # TODO: Consider non-shiftables, add their price according to price curve


def assignment_3():
    prices = [4,  6,  3,  5,  7,  7,  6,  5,  4,  4,  6,  5,  3,  6,  7,  7,  3, 14, 16, 16,  4,  6,  3,  6]
    hours = [x for x in range(0, 24)]
    total = 0
    EV_CHANCE = 0.66  # Assume that 2/3rds of households have EV
    output_dict = {}
    input_list = []
    random_appliances_dict = {'Vacuum': 0.23,
                              'HairDryer': 0.25,
                              'Microwave': 0.6,
                              'PhoneCharger': 0.005,
                              'CeilingFan': 0.075}
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
        l = LpVariable.dict('LaundryMachine', hours, lowBound=0, cat=LpInteger)
        c = LpVariable.dict('ClothesDryer', hours, lowBound=0, cat=LpInteger)
        e = LpVariable.dict('ElectricVehicle', hours, lowBound=0, cat=LpInteger)
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
        problem.addConstraint(lpSum(d1[i] for i in hours) == device_1[1]), 'Device 1 Constraint'
        problem.addConstraint(lpSum(d2[i] for i in hours) == device_2[1]), 'Device 2 Constraint'
        problem.addConstraint(lpSum(d3[i] for i in hours) == device_3[1]), 'Device 3 Constraint'

        problem.solve()
        total += value(problem.objective)
        output_dict[f"Household {i}"] = appliances_list
        input_list.append(create_input(problem))
        """for v in problem.variables():
            print(v.name + " " + str(v.varValue))"""
        print(value(problem.objective))

    values = output_dict.values()
    amount_evs = sum('EV' in item for item in values)
    # print(output_dict)
    # print(input_list)
    create_usage_plots_task_2_3(input_list)
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
    l = LpVariable.dict('LaundryMachine', hours, lowBound=0, cat=LpInteger)
    c = LpVariable.dict('ClothesDryer', hours, lowBound=0, cat=LpInteger)
    e = LpVariable.dict('ElectricVehicle', hours, lowBound=0, cat=LpInteger)
    v = LpVariable.dict('Vacuum', hours, lowBound=0, cat=LpInteger)
    h = LpVariable.dict('HairDryer', hours, lowBound=0, cat=LpInteger)
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
    create_usage_plots_task_4(create_input(problem), L)
    """for v in problem.variables():
        print(v.name + " " + str(v.varValue))"""
    print(value(problem.objective))
    # TODO: Consider non-shiftables, add their price according to price curve
    # TODO: Maybe add normalization for objective function


if __name__ == '__main__':
    assignment_2()