#main project interaction with user 
#CLI

import click
from habit_database import HabitDatabase
from habit import Habit
from datetime import date, datetime
import analysis
import sys

db = HabitDatabase()

@click.group()
def cli():
    """Habit Tracker CLI"""
    click.echo("\n-------Welcome to the Habit Tracker App-------\n")

def exit_app():
    """Exit Application"""
    click.echo("\n---Exiting Application. Goodbye!---")
    sys.exit()

def cli_add_habit():
   """Function to add a habit to the database"""
   while True: 
        name = click.prompt("Please enter a habit name ", type=str)
        description = click.prompt("Please give a short description", type=str)
        periodicity = click.prompt("Please choose between daily, weekly or monthly habit", type=str)
        
        habit = Habit(name=name, description=description, periodicity=periodicity)
        habit.save()
        click.echo(f"\n-----Habit '{habit.name}' added successfully-----")

        if not click.confirm("\nWould you like to add another habit?", default = False):
            click.echo("\n-----Exiting - Returning to Analytics Menu------")
            break

def cli_update_habit():
    """Function to update a habit"""
    while True:
        habits = Habit.get_all_habits()

        if not habits:
            click.echo("\nNo habits found. Please add a habit first.")
            return
        
        click.echo("\nHere are your current habits:")
        click.echo("----------------------------------")
        for habit in habits:
            click.echo(f"Habit id: {habit.habit_id}, Name: {habit.name}")

        while True:
            habit_id = click.prompt("\nPlease enter the id of the habit you like to change", type=int)
            if Habit.habit_exists(habit_id):
                break
            else:
                print(f"\nHabit with id {habit_id} doesn't exist. Please try again.")

        for habit in habits:
            if habit.habit_id == habit_id:
                if click.confirm("\nWould you like to change the name of the habit?"):
                    new_name = click.prompt("Please enter the new name", type=str)
                    habit.update(name = new_name)
                if click.confirm("\nWould you like to change the description?"):
                    new_description = click.prompt("Please enter the new description", type=str)
                    habit.update(description = new_description)
                if click.confirm("\nWould you like to change the periodicity?"):
                    while True:
                        new_periodicity = click.prompt("Please enter the new periodicity", type=str)
                        valid_periodicities={'daily', 'weekly', 'monthly'}
                        if new_periodicity in valid_periodicities:
                            habit.update(periodicity = new_periodicity)
                            break
                        else:
                            click.echo("Please enter a correct periodicity: 'daily', 'weekly' or 'monthly")
                analysis.a1_print_habit(habit)
        
        if not click.confirm("\nWould you like update other habits?", default =False):
            click.echo("\n-----Exiting - Returning to Main Menu------")
            break

def cli_print_all_habits():
    """Function that prints all saved habits"""
    habits = Habit.get_all_habits()
    analysis.a1_print_all_habits(habits)

    click.prompt("Please press Enter to return to the Menu", default='', show_default= False)

def cli_mark_habit_completed():
    """Function to mark a habit as completed"""
    # Get all habits and check that the List is not empty
    while True:
        habits = Habit.get_all_habits()
        if not habits:
            click.echo("\nNo habits found. Please add a habit first.")
            return
        #Display the habits to choose from
        click.echo("\nHere are your current habits:")
        for habit in habits:
            click.echo(f"Habit id: {habit.habit_id}, Name: {habit.name}")
        # Enter the id of the habit that was completed and check if it exists
        while True:
            habit_id = click.prompt("\nPlease enter the id of the habit you would like to mark as completed", type=int) 
            if Habit.habit_exists(habit_id):
                break
            else:
                print(f"\nHabit with id {habit_id} doesn't exist. Please try again.")

        while True:       
            cli_completed_date = click.prompt("Enter the completion date (YYYY-MM-DD) or press Enter to use today's date", default=str(date.today()))

            
            if Habit.correct_date_format(cli_completed_date):
                break
            else:
                print("Wrong date format. Please enter YYYY-MM-DD")
        while True:
            cli_completed_time = click.prompt("Enter the completion time (hh:mm:ss) or press Enter to use the current time.", default=str(datetime.now().time().replace(microsecond=0)))
            
            if Habit.correct_time_format(cli_completed_time):
                break
            else:
                print("Wrong time format. Please enter hh:mm:ss")

     
        for habit in habits:
            if habit.habit_id == habit_id:
                habit.record_completion(completed_date = cli_completed_date, completed_time = cli_completed_time)
       
        if not click.confirm("Would you like to mark another habit as completed?", default =False):
            click.echo("\n-----Exiting - Returning to Main Menu------")
            break

def cli_print_best_performing():
    """Function to print the habits with the longest streak"""
    habits = Habit.get_all_habits()
    analysis.a1_print_best_perfroming_habit(habits)

    click.prompt("Please press Enter to return to the Menu", default='', show_default= False)
        
def cli_print_worst_performing():
    """Function to print the habits with the shortest streak"""
    habits = Habit.get_all_habits()
    analysis.a1_print_worst_performing_habit(habits)

    click.prompt("Please press Enter to return to the Menu", default='', show_default= False)

def cli_print_habit():
    """Function to print a specific habit"""
    while True:
        habits = Habit.get_all_habits()

        click.echo("\nHere are your current habits:")
        for habit in habits:
            click.echo(f"Habit id: {habit.habit_id}, Name: {habit.name}")
        
        while True:
            habit_id = click.prompt("\nPlease enter the id of the habit you would like to view", type=int) 
            if Habit.habit_exists(habit_id):
                break
            else:
                print(f"\nHabit with id {habit_id} doesn't exist. Please try again.")

        habit = Habit.get_by_id(habit_id)
        analysis.a1_print_habit(habit)

        if not click.confirm("Would you like to view another habit?"):
                    click.echo("Returning to Main menu.")
                    break
        
def cli_print_periodicity():
    """Function to print out habits based on their periodicity"""
    while True:
        choice_3 =click.prompt("\nPlease enter 1 for 'daily' or 2 for 'weekly' habits", type=int)

        if choice_3 == 1:
            _cli_print_daily_habits()
        elif choice_3 == 2:
            _cli_print_weekly_habits()
        else:
            click.echo("Invalid input.Please enter a 1 for 'daily' or 2 for 'weekly' habits")
            continue
        if not click.confirm("Would you like to try again?"):
            break

def _cli_print_daily_habits():
    """Helper function that prints out daily habits"""
    habits = Habit.get_all_habits()
    analysis.a1_print_habits_by_periodicity(habits,'daily')
    
def _cli_print_weekly_habits():
    """ Helper function that prints out weekly habits"""
    habits = Habit.get_all_habits()
    analysis.a1_print_habits_by_periodicity(habits,'weekly')

def cli_print_all_longest_streaks():
    """Print longest streaks of all habits
    """
    habits = Habit.get_all_habits()
    analysis.a1_print_longest_streak(habits)

def cli_print_habit_streaks():

    while True:
        habits = Habit.get_all_habits()

        click.echo("\nHere are your current habits:")
        for habit in habits:
            click.echo(f"Habit id: {habit.habit_id}, Name: {habit.name}")
        
        while True:
            habit_id = click.prompt("\nPlease enter the id of the habit you would like to view", type=int) 
            if Habit.habit_exists(habit_id):
                break
            else:
                print(f"\nHabit with id {habit_id} doesn't exist. Please try again.")

        habit = Habit.get_by_id(habit_id)
        analysis.a1_print_streaks(habit)

        if not click.confirm("Would you like to view another habit?"):
            click.echo("Returning to Main menu.")
            break

@cli.command()
def main_menu():
    """Start Main Menu for managing habits"""
    while True:
            click.echo("\n_____Main MENU_____")
            click.echo("\nWhat would you like to do?")
            click.echo("    1. Add a habit")
            click.echo("    2. Update habit")
            click.echo("    3. Mark habit as completed")
            click.echo("    4. Analyse habits")
            click.echo("    5. Exit")

            choice = click.prompt("Please enter your choice (1-5)", type=int)

            if choice == 1:
                cli_add_habit()
            
            elif choice == 2:
                cli_update_habit()

            elif choice == 3: 
                cli_mark_habit_completed()

            elif choice == 4:
                analysation_mode()

            elif choice == 5:
                exit_app()

            else:
                click.echo("Invalid choice. Please enter a number between 1 and 6.")


def analysation_mode(): 
    """Start Analytics Module"""
    while True:
                    click.echo("\n_____ANALYTICS MENU_____")
                    click.echo("\nWhat would you like to do?")
                    click.echo("    1. Check for best performing habit(s)")
                    click.echo("    2. Check for worst performing habit(s)")
                    click.echo("    3. View all habits")
                    click.echo("    4. View a habit's information")
                    click.echo("    5. View habits based on periodicity")
                    click.echo("    6. View streak data of a habit")
                    click.echo("    7. View all my longest streaks")
                    click.echo("    8. Return to main menu")
                    click.echo("    9. Exit\n")

                    choice_2 = click.prompt("Please enter your choice (1-9)", type=int)
                    
                    if choice_2 == 1:

                        cli_print_best_performing()

                    elif choice_2 == 2:
                   
                        cli_print_worst_performing()
                    
                    elif choice_2 == 3:

                        cli_print_all_habits()

                    elif choice_2 == 4:

                        cli_print_habit()

                    elif choice_2 == 5:
                        cli_print_periodicity()

                    elif choice_2== 6:
                        cli_print_habit_streaks()

                    elif choice_2 == 7:
                        cli_print_all_longest_streaks()
                    
                    elif choice_2 == 8:
                        return
                    
                    elif choice_2 == 9:
                        exit_app()

                    else:
                        click.echo("Invalid choice. Please enter a number between 1 and 6.")
                        continue

if __name__ == '__main__':
    cli()