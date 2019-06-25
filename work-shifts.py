import datetime

from collections import namedtuple
from enum import IntEnum

class Role(IntEnum):
    """
    Each of the different roles that need to be fulfilled through the schedule
    """
    GET_DRINKS = 0
    DRINKS_BAR = 1
    DRINKS_BAR_COORDINATOR = 2
    DRINKS_TICKETS = 3
    KITCHEN = 4
    KITCHEN_COORDINATOR = 5
    FOODS_BAR = 6
    FOODS_BAR_COORDINATOR = 7
    FOODS_TICKETS = 8

class ShiftTime(IntEnum):
    """
    Each of the different shift times in a day in the schedule.
    NIGHT_NORMAL and NIGHT_LONG are mutually exclusive (some days are long and
    some are of normal duration)
    """
    MORNING = 1
    EVENING = 2
    NIGHT_NORMAL = 3
    NIGHT_LONG = 4

"""
A shift which has been assigned to a group
"""
Assigned_Shift = namedtuple('Assigned_Shift', ['group', 'shift'])

# Weight of each role (some roles are considered heavier than others because
# they are more exhausting)
ROLE_WEIGHTS = {
    Role.GET_DRINKS: 1,
    Role.DRINKS_BAR: 1,
    Role.DRINKS_BAR_COORDINATOR: 1.2,
    Role.DRINKS_TICKETS: 1,
    Role.KITCHEN: 1,
    Role.KITCHEN_COORDINATOR: 1.2,
    Role.FOODS_BAR: 1,
    Role.FOODS_BAR_COORDINATOR: 1.2,
    Role.FOODS_TICKETS: 1
}

# Weight of each time of the day (some shift times are considered heavier than
# others because they are longer)
TIME_WEIGHTS = {
    ShiftTime.MORNING: 0.5,
    ShiftTime.EVENING: 1,
    ShiftTime.NIGHT_NORMAL: 1,
    ShiftTime.NIGHT_LONG: 1.2
}

# Number of groups that need to fill the schedule
NUMBER_OF_GROUPS = 12

# Number of days of normal length
NUMBER_OF_NORMAL_DAYS = 2

# Number of days longer than normal days
NUMBER_OF_LONG_DAYS = 2

# The first date of the schedule to be filled
START_DATE = datetime.datetime.strptime('10/08/2019', '%d/%m/%Y')

# The last date of the schedule to be filled
END_DATE = START_DATE + datetime.timedelta(
    days=(NUMBER_OF_LONG_DAYS + NUMBER_OF_NORMAL_DAYS))

class Shift:
    """
    Class representing a shift to be covered in a schedule
    """
    def __init__(self, role, time):
        self.role = role
        self.time = time
        self.weight = ROLE_WEIGHTS[self.role]*TIME_WEIGHTS[self.time]

    def __eq__(self, other):
        return (self.role == other.role
                    and self.time == other.time
                    and self.weight == other.weight)

    def __hash__(self):
        return hash((self.role, self.time, self.weight))

# Shifts that need to be covered in a normal day
SHIFTS_IN_NORMAL_DAY = {
    Shift(Role.GET_DRINKS, ShiftTime.MORNING): 3,
    Shift(Role.DRINKS_BAR, ShiftTime.EVENING): 4,
    Shift(Role.DRINKS_BAR_COORDINATOR, ShiftTime.EVENING): 1,
    Shift(Role.DRINKS_TICKETS, ShiftTime.EVENING): 2,
    Shift(Role.KITCHEN, ShiftTime.EVENING): 5,
    Shift(Role.KITCHEN_COORDINATOR, ShiftTime.EVENING): 1,
    Shift(Role.FOODS_BAR, ShiftTime.EVENING): 5,
    Shift(Role.FOODS_BAR_COORDINATOR, ShiftTime.EVENING): 1,
    Shift(Role.FOODS_TICKETS, ShiftTime.EVENING): 4,
    Shift(Role.DRINKS_BAR, ShiftTime.NIGHT_NORMAL): 4,
    Shift(Role.DRINKS_BAR_COORDINATOR, ShiftTime.NIGHT_NORMAL): 1,
    Shift(Role.DRINKS_TICKETS, ShiftTime.NIGHT_NORMAL): 2,
    Shift(Role.KITCHEN, ShiftTime.NIGHT_NORMAL): 5,
    Shift(Role.KITCHEN_COORDINATOR, ShiftTime.NIGHT_NORMAL): 1,
    Shift(Role.FOODS_BAR, ShiftTime.NIGHT_NORMAL): 5,
    Shift(Role.FOODS_BAR_COORDINATOR, ShiftTime.NIGHT_NORMAL): 1,
    Shift(Role.FOODS_TICKETS, ShiftTime.NIGHT_NORMAL): 4
}

# Shifts that need to be covered in a long day
SHIFTS_IN_LONG_DAY = {
    Shift(Role.GET_DRINKS, ShiftTime.MORNING): 3,
    Shift(Role.DRINKS_BAR, ShiftTime.EVENING): 4,
    Shift(Role.DRINKS_BAR_COORDINATOR, ShiftTime.EVENING): 1,
    Shift(Role.DRINKS_TICKETS, ShiftTime.EVENING): 2,
    Shift(Role.KITCHEN, ShiftTime.EVENING): 5,
    Shift(Role.KITCHEN_COORDINATOR, ShiftTime.EVENING): 1,
    Shift(Role.FOODS_BAR, ShiftTime.EVENING): 5,
    Shift(Role.FOODS_BAR_COORDINATOR, ShiftTime.EVENING): 1,
    Shift(Role.FOODS_TICKETS, ShiftTime.EVENING): 4,
    Shift(Role.DRINKS_BAR, ShiftTime.NIGHT_LONG): 4,
    Shift(Role.DRINKS_BAR_COORDINATOR, ShiftTime.NIGHT_LONG): 1,
    Shift(Role.DRINKS_TICKETS, ShiftTime.NIGHT_LONG): 2,
    Shift(Role.KITCHEN, ShiftTime.NIGHT_LONG): 5,
    Shift(Role.KITCHEN_COORDINATOR, ShiftTime.NIGHT_LONG): 1,
    Shift(Role.FOODS_BAR, ShiftTime.NIGHT_LONG): 5,
    Shift(Role.FOODS_BAR_COORDINATOR, ShiftTime.NIGHT_LONG): 1,
    Shift(Role.FOODS_TICKETS, ShiftTime.NIGHT_LONG): 4
}


def print_weight_of_each_group(assigned_shifts):
    """
    Debug function. Prints the total weight of the shifts assigned to each
    group
    """
    print('Weight of each group:')
    for group in assigned_shifts.keys():
       weight = 0
       for shift_model, number in assigned_shifts[group].items():
           weight += number * shift_model.weight
       print('%d: %.2f' % (group, weight))


def print_shifts_of_each_group(assigned_shifts):
    """
    Debug function. Prints the shifts assigned to each group
    """
    for group in assigned_shifts.keys():
       weight = 0
       for shift_model, number in assigned_shifts[group].items():
           weight += number * shift_model.weight

       print('Group %d (weight: %.2f):' % (group, weight))
       all_shift_types = sorted(assigned_shifts[group].keys(),
                                key=lambda s: (s.time, s.role))

       for shift_model in all_shift_types:
           print('\t\t%s - %s: %d'
                 % (shift_model.time,
                    shift_model.role,
                    assigned_shifts[group][shift_model]))
       print('-------------------')


def print_weight_of_each_group_per_day(assigned_shifts_per_day):
    """
    Debug function. Prints the weight of each group per day
    """
    for day in sorted(assigned_shifts_per_day.keys()):
        assigned_shifts = assigned_shifts_per_day[day]
        sorted_assigned_shifts = sorted(
            assigned_shifts,
            key=lambda s: (s.shift.time, s.shift.role, s.group))

        print('Day %s:' % day)
        for group in range(1, NUMBER_OF_GROUPS + 1):
            print('\tGroup %d: %.2f' % (group, sum((s.shift.weight for s in assigned_shifts if s.group == group))))
        print('------------------------')


def main():
    # Initialise the list of assigned shifts
    assigned_shifts = {}
    for i in range(0, NUMBER_OF_GROUPS):
        assigned_shifts[i+1] = dict()

    # All shifts that need to be covered
    # {Shift: number_of_shifts_of_this_type}
    all_shifts = dict()
    for k, v in SHIFTS_IN_NORMAL_DAY.items():
        all_shifts[k] = v*NUMBER_OF_NORMAL_DAYS

    for k,v in SHIFTS_IN_LONG_DAY.items():
        if k in all_shifts:
            all_shifts[k] += v*NUMBER_OF_LONG_DAYS
        else:
            all_shifts[k] = v*NUMBER_OF_LONG_DAYS

    # First of all, assign shifts equally (number_of_shifts / NUMBER_OF_GROUPS
    # to each group). Store the remaining shifts (number_of_shits %
    # NUMBER_OF_GROUPS) in this variable.
    remaining_shifts = []
    for shift, number in all_shifts.items():
        if number % NUMBER_OF_GROUPS != 0:
            for i in range(0, number % NUMBER_OF_GROUPS):
                remaining_shifts.append(shift)

        number_for_group = int(number / NUMBER_OF_GROUPS)
        if number_for_group != 0:
            for group in assigned_shifts.keys():
                assigned_shifts[group][shift] = number_for_group

    # To assign the remaining shifts, we will use a greedy algorithm: sort all
    # shifts by weight, and then assign them iteratively to whichever group is
    # pulling the lowest weight
    remaining_shifts = sorted(
        remaining_shifts,
        key=lambda s: (s.weight, s.role, s.time),
        reverse=True)

    for shift in remaining_shifts:
        # Find one with the lowest weight at the moment
        min_group = None
        min_sum = None
        for group in assigned_shifts.keys():
            weight = 0
            for shift_model, number in assigned_shifts[group].items():
                weight += number * shift_model.weight

            if not min_sum or weight < min_sum:
                min_sum = weight
                min_group = group

        if shift in assigned_shifts[min_group]:
            assigned_shifts[min_group][shift] += 1
        else:
            assigned_shifts[min_group][shift] = 1

    # Groups already have their shifts, but they have not been distributed
    # along the different days
    # {date: list(Assigned_Shift)}
    assigned_shifts_per_day = dict()
    for i in range(0, (END_DATE - START_DATE).days):
        d = START_DATE + datetime.timedelta(days=i)

        assigned_shifts_per_day[d.strftime('%d/%m/%Y')] = []

    # Distribute the days using a greedy algorithm: iterate over each day and
    # assign the shifts of the group which is working less that at that point
    # that day.
    # If we try to optimize each group individually, the groups that come last
    # will have less options and will be grossly overworked and underworked in
    # different days.
    for i, day in enumerate(sorted(assigned_shifts_per_day.keys())):
        # Assume that the first NUMBER_OF_LONG_DAYS are the long days
        is_long_day = (i < NUMBER_OF_LONG_DAYS)
        shifts_to_cover = (SHIFTS_IN_LONG_DAY if is_long_day
                           else SHIFTS_IN_NORMAL_DAY)

        for shift, number_of_shifts in shifts_to_cover.items():
            for shift_number in range(0, number_of_shifts):

                # Groups which could potentially cover this shift
                candidates = set()
                for group in assigned_shifts.keys():
                    if (shift in assigned_shifts[group]
                            and assigned_shifts[group][shift] > 0):
                        candidates.add(group)

                # From all the groups which could cover this shift, choose the
                # one which is the least overworked in this particular shift
                min_weight_all_day = 0
                min_weight_this_time = 0
                min_group = None

                for group in candidates:
                    weight_all_day = sum(
                        (s.shift.weight for s in assigned_shifts_per_day[day]
                         if s.group == group))

                    weight_this_time = sum(
                        (s.shift.weight for s in assigned_shifts_per_day[day]
                         if s.group == group and s.shift.time == shift.time))

                    if (not min_group
                            or weight_this_time < min_weight_this_time
                            or (weight_this_time == min_weight_this_time
                                and weight_all_day < min_weight_all_day)):
                        min_weight_all_day = weight_all_day
                        min_weight_this_time = weight_this_time
                        min_group = group

                assigned_shifts_per_day[day].append(
                    Assigned_Shift(group=min_group, shift=shift))

                # Remove the assigned shift from the pool
                assigned_shifts[min_group][shift] -= 1

    # Print the results
    for day in sorted(assigned_shifts_per_day.keys()):
        assigned_shifts = assigned_shifts_per_day[day]
        sorted_assigned_shifts = sorted(
            assigned_shifts,
            key=lambda s: (s.shift.time, s.shift.role, s.group))

        print('Day %s:' % day)
        for assigned_shift in sorted_assigned_shifts:
            print('\t\t%s - %s: Group %d' % (assigned_shift.shift.time, assigned_shift.shift.role, assigned_shift.group))
        print('------------------------')


if __name__ == '__main__':
    main()
