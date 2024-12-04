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
            print(f"{i}. '{habit.name}' with a streak of {habit.longest_streak} days.")
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
            print(f"{i}. '{habit.name}' with a streak of {habit.longest_streak} days.")

        print("-----------------End------------------")
        print("\n")

def a1_print_longest_streak(habit):
    """
    Prints out the longest current streak of a given habit

    Args:
        habit (Habit): Habit whose streak should be printed out
    """
    if habit.periodicity == 'weekly':
        local_periodicity = 'weeks'
    elif habit.periodicity == 'daily':
        local_periodicity = 'days'

    if habit.longest_streak == 0:
        print("\nYou have not completed this habit yet. Try harder!")
    else:
        print(f"\nYour longest streak for '{habit.name}' is {habit.longest_streak} {local_periodicity}")

def a1_print_habits_by_periodicity(habits: List['Habit'], wanted_periodicity: str):
    """
    Prints out all habits of a given periodicity

    Args:
        habits (List[Habit]): List of all current habits
        wanted_periodicity (str): Either 'daily' or 'weekly'
    """
    if wanted_periodicity not in ('weekly','daily') :
        print("\nPlease enter either weekly or daily\n")
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



