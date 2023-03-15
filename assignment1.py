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


def create_usage_plots_task_2(lst: list):
    """Draws a stacked bar chart for the use of household appliances in a neighborhood."""
    variables_list = [[item[0] for item in items] for items in lst]
    flat_list = flatten(variables_list)
    count_dict = {}
    ev = np.zeros(24)
    vacuum = np.zeros(24)
    dryer = np.zeros(24)
    laundry = np.zeros(24)
    dishwasher = np.zeros(24)
    hairdryer = np.zeros(24)
    microwave = np.zeros(24)
    phone = np.zeros(24)
    for l in flat_list:
        if l not in count_dict.keys():
            count_dict[l] = flat_list.count(l)
    for k, v in count_dict.items():
        _, k_2 = k.split("_")
        k_2 = int(k_2)
        if 'electric' in k.lower():
            ev[k_2] = v
        elif 'vacuum' in k.lower():
            vacuum[k_2] = v
        elif 'dryer' in k.lower():
            dryer[k_2] = v
        elif 'laundry' in k.lower():
            laundry[k_2] = v
        elif 'dish' in k.lower():
            dishwasher[k_2] = v
        elif 'microwave' in k.lower():
            microwave[k_2] = v
        elif 'hair' in k.lower():
            hairdryer[k_2] = v
    values = {
        "EV": ev,
        "Vacuum": vacuum,
        "Dryer": dryer,
        "Laundry Machine": laundry,
        "Dishwasher": dishwasher,
        "Microwave": microwave,
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


# Assignment 2
def assignment_2():
    prices = [4,  6,  3,  5,  7,  7,  6,  5,  4,  4,  6,  5,  3,  6,  7,  7,  3, 14, 16, 16,  4,  6,  3,  6]
    problem = LpProblem('Demand Response', LpMinimize)
    hours = [x for x in range(0, 24)]
    d = LpVariable.dict('Dishwasher', hours, lowBound=0)
    l = LpVariable.dict('LaundryMachine', hours, lowBound=0)
    c = LpVariable.dict('ClothesDryer', hours, lowBound=0)
    e = LpVariable.dict('ElectricVehicle', hours, lowBound=0)
    v = LpVariable.dict('Vacuum', hours, lowBound=0)
    h = LpVariable.dict('HairDryer', hours, lowBound=0)
    m = LpVariable.dict('Microwave', hours, lowBound=0)

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
    create_usage_plots_task_2([create_input(problem)])

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
        d = LpVariable.dict('Dishwasher', hours, lowBound=0)
        l = LpVariable.dict('LaundryMachine', hours, lowBound=0)
        c = LpVariable.dict('ClothesDryer', hours, lowBound=0)
        e = LpVariable.dict('ElectricVehicle', hours, lowBound=0)
        d1 = LpVariable.dict(device_1[0], hours, lowBound=0) # device 1
        d2 = LpVariable.dict(device_2[0], hours, lowBound=0) # device 2
        d3 = LpVariable.dict(device_3[0], hours, lowBound=0) # device 3

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
        print(value(problem.objective))

    values = output_dict.values()
    print(values)
    amount_evs = sum('EV' in item for item in values)
    Vacuum = sum('Vacuum' in item for item in values)
    Microwave = sum('Microwave' in item for item in values)
    HairDryer = sum('HairDryer' in item for item in values)
    PhoneCharger = sum('PhoneCharger' in item for item in values)
    CeilingFan = sum('CeilingFan' in item for item in values)
    create_usage_plots_task_2_3(input_list)
    print(f"Amount of EVs: {amount_evs}, Vacuum {Vacuum}, HairDryer {HairDryer} PhoneCharger {PhoneCharger} CeilingFan {CeilingFan} Microwave {Microwave}")
    print(f"Share of electric vehicles: {amount_evs/30}")
    print(f"Total price of all households for the day: {total}")  # Total price of all households over the day
    # TODO: Consider non-shiftables, add their price according to price curve
    # Since we don't have to consider grid load, every household can use the same appliances at the same time
    # to save money (everyone uses the optimal solution).

def non_shiftables_task_basic():
    prices = [4, 6, 3, 5, 7, 7, 6, 5, 4, 4, 6, 5, 3, 6, 7, 7, 3, 14, 16, 16, 4, 6, 3, 6]
    consumption_per_hour = [0.0 for x in range(0, 24)]
    price_for_non_shiftable = [0.0 for x in range(0, 24)]
    # price for non-shiftable devices are fixed that the price for the non-shiftable devices
    # is the same in task 2 and 4
    lightning = 1.5/10 # usage per hour between 10.00 - 20.00
    heating = 8/24 # 24/7
    refrigerator = 2.64/24 #24/7 household has two refigerators
    electric_stove = 3.9 /2 # on 18 and 19
    tv = 0.4 /5  # in this example tv is on between 18.00 - 23.00
    computers = 1.8/5 # in this task 3 computers, are on between 18.00 - 23.00

    for i in range(len(consumption_per_hour)):
        fixed_consumption_per_hour = heating + refrigerator
        if 9 <= i <= 19:
            fixed_consumption_per_hour = fixed_consumption_per_hour + lightning
        if 17 <= i <= 22:
            fixed_consumption_per_hour = fixed_consumption_per_hour + tv + computers
        if 18 <= i <= 19:
            fixed_consumption_per_hour = fixed_consumption_per_hour + electric_stove

        consumption_per_hour[i] = fixed_consumption_per_hour
        price_for_non_shiftable[i] = prices[i] * fixed_consumption_per_hour
    total_price = np.sum(price_for_non_shiftable)
    print('Price for non-shiftable devices: ', total_price)
    return consumption_per_hour, price_for_non_shiftable






def assignment_4():
    non_shiftable_consumption, non_shiftable_prices = non_shiftables_task_basic()
    prices = [4, 6, 3, 5, 7, 7, 6, 5, 4, 4, 6, 5, 3, 6, 7, 7, 3, 14, 16, 16, 4, 6, 3, 6]
    problem = LpProblem('Demand Response', LpMinimize)
    hours = list(range(24))
    L = 9
    d = LpVariable.dict('Dishwasher', hours, lowBound=0, cat='Continuous')
    l = LpVariable.dict('LaundryMachine', hours, lowBound=0, cat='Continuous')
    c = LpVariable.dict('ClothesDryer', hours, lowBound=0, cat='Continuous')
    e = LpVariable.dict('ElectricVehicle', hours, lowBound=0, cat='Continuous')
    v = LpVariable.dict('Vacuum', hours, lowBound=0, cat='Continuous')
    h = LpVariable.dict('HairDryer', hours, lowBound=0, cat='Continuous')
    m = LpVariable.dict('Microwave', hours, lowBound=0, cat='Continuous')

    # Objective function
    problem += lpSum(
        [(prices[i] * (d[i] + l[i] + c[i] + e[i] + v[i] + h[i] + m[i])) for i in hours])

    # Constraints
    problem.addConstraint(lpSum(d[i] for i in hours) == 1.44), 'Dishwasher Constraint'
    problem.addConstraint(lpSum(l[i] for i in hours) == 1.94), 'Laundry Machine Constraint'
    problem.addConstraint(lpSum(c[i] for i in hours) == 2.5), 'Clothes Dryer Constraint'
    problem.addConstraint(lpSum(e[i] for i in hours) == 9.9), 'Electric Vehicle Constraint'
    problem.addConstraint(lpSum(v[i] for i in hours) == 0.23), 'Vacuum Constraint'
    problem.addConstraint(lpSum(h[i] for i in hours) == 0.25), 'Hair Dryer Constraint'
    problem.addConstraint(lpSum(m[i] for i in hours) == 0.6), 'Microwave Constraint'
    for i in hours:
        problem.addConstraint(d[i] + l[i] + c[i] + e[i] + v[i] + h[i] + m[i] <= L-non_shiftable_consumption[i]), 'Maximum Load Constraint'

    problem.solve()

    create_usage_plots_task_4(create_input(problem), L)
    print(value(problem.objective))
    # TODO: Consider non-shiftables, add their price according to price curve


if __name__ == '__main__':
    assignment_3()
    # non_shiftables_task_basic()