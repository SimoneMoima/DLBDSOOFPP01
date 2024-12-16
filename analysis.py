from typing import List
from habit import Habit

def a1_print_all_habits(habits: List['Habit']):
    """Prints a record of all habits in the provided list.

    Args:
        habits (List[Habits]): Contains a List of Habit objects
    """
    if not habits:
        print("No habits found.")
        return
    
    print("\nHabit Records:")
    for habit in habits:
        print("-----------------------------------")
        print(f"Habit id:       {habit.habit_id}")
        print(f"Name:           {habit.name}")
        print(f"Description:    {habit.description}")
        print(f"Periodicity:    {habit.periodicity}")
        print(f"Creation Date:  {habit.creation_date}")
        print(f"Creation Time:  {habit.creation_time}")
        print(f"Current Streak: {habit.current_streak}")
        print(f"Longest Streak: {habit.longest_streak}")
        print("-----------------------------------")
    print("\nEnd of Habit Records\n")

def a1_print_habit(habit):
        
        print("\nHabit Record:")
        print("-----------------------------------")
        print(f"Habit id:       {habit.habit_id}")
        print(f"Name:           {habit.name}")
        print(f"Description:    {habit.description}")
        print(f"Periodicity:    {habit.periodicity}")
        print(f"Creation Date:  {habit.creation_date}")
        print(f"Creation Time:  {habit.creation_time}")
        print(f"Current Streak: {habit.current_streak}")
        print(f"Longest Streak: {habit.longest_streak}")
        print("-----------------------------------")
        print("\nEnd of Habit Record\n")

def a1_print_best_perfroming_habit(habits: List['Habit']):
    """
    Print out the current best perfoming habit

    :param habits (List[Habit]): List of all current habits
    """
    if not habits:
        print("No habits found. ")
        return
    
    best_performing_habit = []
    longest_streak= 0

    for habit in habits:
        streak = int(habit.longest_streak)
        if streak > longest_streak:
            longest_streak = streak
            best_performing_habit = [(habit)]
        elif streak == longest_streak:
            best_performing_habit.append(habit)


    if best_performing_habit:
        print("\nYour best performing habit(s) are: ")
        print("--------------------------------------")
        for i,habit in enumerate(best_performing_habit, start=1):
            period = _transform_periodicity(habit.longest_streak, habit.periodicity)
            print(f"{i}. '{habit.name}' with a streak of {habit.longest_streak} {period}.")
        print("---------------End--------------------")
        print("\n")
        
    else:
        print("\nYou have not completed a streak yet.")

def a1_print_worst_performing_habit(habits: List['Habit']):
    """
    Print out the worst performing habit

    Args:
        habits (List[Habit]): List of all current habits
    """
    if not habits:
        print("No habits found. ")
        return
    
    worst_performing_habit = []
    shortest_streak= 0

    for habit in habits:
        streak = habit.longest_streak
        if streak < shortest_streak:
            shortest_streak = streak
            worst_performing_habit = [(habit)]
        elif streak == shortest_streak:
            worst_performing_habit.append(habit)

    if worst_performing_habit:
        print("\nYour worst performing habit(s) are: ")
        print("--------------------------------------")
        for i, habit in enumerate(worst_performing_habit, start=1):
            period = _transform_periodicity(habit.longest_streak, habit.periodicity)
            print(f"{i}. '{habit.name}' with a streak of {habit.longest_streak} {period}.")

        print("-----------------End------------------")
        print("\n")

def _transform_periodicity(streak, periodicity):
    """Helper function to print periodicities correctly
        monthly -> month(s)
        daily -> day(s)
        weekly -> week(S)
        if streak > 1 an 's' is added

    Args:
        streak (int): streak data as integer
        periodicity (str): periodicity of the habit

    Returns:
        str: week(s), day(s), month(s) accordingly
    """

    if streak == 1:
        if periodicity == 'weekly':
            period = 'week'
        elif periodicity == 'daily':
            period = 'day'
        elif periodicity == 'monthly':
            period = 'month'
    else:
        if periodicity == 'weekly':
            period = 'weeks'
        elif periodicity == 'daily':
            period = 'days'
        elif periodicity == 'monthly':
            period = 'months'
    return period

def a1_print_longest_streak(habits: List['Habit']):
    """
    Prints out the longest streaks of all habits

    Args:
        habit (Habit): Habit whose streak should be printed out
    """
    print("\nYour longest streaks are:")
    print("-----------------------------------")

    for habit in habits:

        period = _transform_periodicity(habit.longest_streak, habit.periodicity)

        if habit.longest_streak == 0:
            print(f"'{habit.name}'  : You have not completed this habit yet. Try harder, you can do it!")
        else:
            print(f"'{habit.name}'  : {habit.longest_streak} {period}")

    print("----------------END----------------")

def a1_print_habits_by_periodicity(habits: List['Habit'], wanted_periodicity: str):
    """
    Prints out all habits of a given periodicity

    Args:
        habits (List[Habit]): List of all current habits
        wanted_periodicity (str): Either 'daily' or 'weekly'
    """
    if wanted_periodicity not in ('weekly','daily', 'monthly') :
        print("\nPlease enter either weekly, monthly or daily\n")
        return
    
    filter_habits = [habit for habit in habits if habit.periodicity == wanted_periodicity]

    print(f"\nYour {wanted_periodicity} habits are: ")
    print("--------------------------------------")
    
    if filter_habits:
        for i, habit in enumerate(filter_habits, start=1):
            print(f" {i}. {habit.name}")
    else:
        print(f"\nNo {wanted_periodicity} habits found.")
        
  
    print("-----------------End------------------")
    print("\n")

def a1_print_streaks(habit):
    """Function to print the current and longest streak of a habit

    Args:
        habit (List): habit that should be displayed
    """
     
    period_current = _transform_periodicity(habit.current_streak, habit.periodicity)
    period_longest = _transform_periodicity(habit.longest_streak, habit.periodicity)
    if habit.current_streak == 0:
        print("\nYou have not completed this habit yet. Try harder, you can do it!\n")
    else:
        print("--------------------------------------")
        print(f"\nYour current streak of '{habit.name}' is {habit.current_streak} {period_current}.")
        print(f"Your longest streak of '{habit.name}' is {habit.longest_streak} {period_longest} ")
        print("--------------------------------------")

