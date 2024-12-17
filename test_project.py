from calendar import month
import analysis
from habit_database import HabitDatabase
from habit import Habit
from datetime import date, timedelta
import pytest


class TestHabit:

  def setup_method(self): 
    self.db = HabitDatabase("test.db")
    self.db.db_clear_tables()
  
  def test_habit_class(self):    
    #5 predefined habits
    #Habit - Daily/ Streak = 7
    habit = Habit(name="Drink more tea", 
                  description="drink at least one cup of healthy tea a day", 
                  periodicity="daily", 
                  creation_date="2024-10-31",
                  db=self.db
                  )
    habit.save()
    habit.record_completion(str(date.today()-timedelta(days=6)) , "17:30:16")
    habit.record_completion(str(date.today()-timedelta(days=5)), "16:38:58")
    habit.record_completion(str(date.today()-timedelta(days=4)), "09:12:56")
    habit.record_completion(str(date.today()-timedelta(days=3)), "12:06:06")
    habit.record_completion(str(date.today()-timedelta(days=2)), "12:06:06")
    habit.record_completion(str(date.today()-timedelta(days=1)),"17:30:16")
    habit.record_completion(str(date.today()), "16:38:58")
    habit.calculate_daily_streak()

    #Assertions to ensure data is saved correctly and the current and longest streak are calculated correctl
    assert habit.name == "Drink more tea"
    assert habit.description == "drink at least one cup of healthy tea a day"
    assert habit.periodicity == "daily"
    assert habit.creation_date == "2024-10-31"
    assert habit.current_streak == 7
    assert habit.longest_streak == 7
    
    #Habit 2 - Weekly/streak = 3
    habit2 = Habit(name="Running", 
                   description="Run 5km", 
                   periodicity="weekly", 
                   creation_date="2024-11-01", 
                   db=self.db
                   )
    habit2.save()
    habit2.record_completion(str(date.today()-timedelta(weeks=7)), "09:12:56") 
    habit2.record_completion(str(date.today()-timedelta(weeks=6)), "09:12:56") 
    habit2.record_completion(str(date.today()-timedelta(weeks=5)), "09:12:56")    
    habit2.record_completion(str(date.today()-timedelta(weeks=4)), "09:12:56")  
    habit2.record_completion(str(date.today()-timedelta(weeks=2)), "09:12:56")
    habit2.record_completion(str(date.today()-timedelta(weeks=1)), "12:06:06")
    habit2.record_completion(completed_time="12:06:06") #uses the internal date to set it to today
    habit2.calculate_weekly_streak()

    #Habit 3 - Weekly/ streak = 6
    habit3 = Habit(name="Clean kitchen cupboards", 
                   description="clean the inside of the kitchen cupboards", 
                   periodicity="weekly", 
                   creation_date="2024-09-18",
                   db=self.db
                   )
    habit3.save()  
    habit3.record_completion(str(date.today()-timedelta(weeks=5)),"17:30:16")
    habit3.record_completion(str(date.today()-timedelta(weeks=4)), "16:38:58")
    habit3.record_completion(str(date.today()-timedelta(weeks=3)), "09:12:56")
    habit3.record_completion(str(date.today()-timedelta(weeks=2)), "09:12:56")
    habit3.record_completion(str(date.today()-timedelta(weeks=1)), None)
    habit3.record_completion()
    habit3.calculate_weekly_streak()
   
    #Habit 4 - Daily/ streak = 5
    habit4 = Habit(name="Brush dog", 
                   description="Brush my dogs hair once a day", 
                   periodicity="daily", 
                   creation_date="2024-11-11", 
                   db=self.db
                   )
    habit4.save()  
    habit4.record_completion(str(date.today()-timedelta(days=4)),"17:30:16")
    habit4.record_completion(str(date.today()-timedelta(days=3)), "16:38:58")
    habit4.record_completion(str(date.today()-timedelta(days=2)), "09:12:56")
    habit4.record_completion(str(date.today()-timedelta(days=1)), "12:06:06")
    habit4.record_completion() #current date,time
    habit4.record_completion() #Test Error message habit already completed today
    habit4.calculate_daily_streak()

    #Habit 5 - Daily/ streak = 5 / Test double entry
    habit5 = Habit("Meditate", 
                   "Meditate for 15 minutes a day", 
                   "daily", "2024-10-13", 
                   None, 
                   self.db
                   )
    habit5.save() 
    habit5.record_completion("2024-10-13", "12:06:06")
    habit5.record_completion(str(date.today()-timedelta(days=4)),"17:30:16")
    habit5.record_completion(str(date.today()-timedelta(days=4)),"17:30:16")
    habit5.record_completion(str(date.today()-timedelta(days=3)), "16:38:58")
    habit5.record_completion(str(date.today()-timedelta(days=2)), "09:12:56")
    habit5.record_completion(str(date.today()-timedelta(days=1)), "12:06:06")
    habit5.record_completion()
    habit5.calculate_daily_streak()

    
    #Habit 8 - Monthly 
    habit8 = Habit("Clean cupboard", 
                   "Clean all kitchen cupboards, dont forget to take out all dishes",
                   "monthly",
                   None,
                   None,
                   self.db
                   )
    habit8.save()
    habit8.record_completion(str(date.today()-timedelta(weeks=16)), "12:06:06")
    habit8.record_completion(str(date.today()-timedelta(weeks=12)), "12:06:06")
    habit8.record_completion(str(date.today()-timedelta(weeks=8)), "12:06:06")
    habit8.record_completion(str(date.today()-timedelta(weeks=4)), "12:06:06")
    habit8.record_completion() 

    assert habit8.longest_streak == 5

    #Habit 6 - Daily / Not completed, streak = 0
    habit6 = Habit("Sleep 8 hours", 
                   "Sleep 8 hours a day", 
                   "daily", 
                   None, 
                   None, 
                   self.db)
    habit6.save()
    habit4.calculate_daily_streak()

    #Test the save function
    habit7 = Habit(name="Running", 
                   description="Run 5km", 
                   periodicity="weekly", 
                   creation_date="2024-11-01", 
                   db=self.db)
    with pytest.raises(ValueError):
      habit7.save() #Habit already exists

    habit7 = Habit( name ="",
                   description="Run 5km", 
                   periodicity="weekly", 
                   creation_date="2024-11-01", 
                   db=self.db)
    with pytest.raises(ValueError):
      habit7.save() # Name empty
    
    habit7 = Habit( name ="Do fun stuff",
                   description="Do something that makes you laugh out loud.", 
                   periodicity="dail", 
                   creation_date="2024-11-01", 
                   db=self.db)
    with pytest.raises(ValueError):
      habit7.save() #Incorrect periodicity

    #Test delete function
    habit2.delete_habit(habit2.habit_id, self.db)
    assert Habit.habit_exists(habit2.habit_id, self.db) is False

    #Test update function
    habit2.update(name = "Run",
                  description= "Run 4km in a week.",
                  periodicity= "daily")
    assert habit2.name == "Run"
    assert habit2.description =="Run 4km in a week."
    assert habit2.periodicity == "daily"

    #Test delete habit function and ensure functions give error message if habit doesnt exist
    habit7 = Habit(name ="Do fun stuff",
                   description="Do something that makes you laugh out loud.", 
                   periodicity="daily", 
                   creation_date="2024-11-01", 
                   db=self.db)
    habit7.save()
    assert habit7.name == "Do fun stuff"  #Ensures habit7 was saved
    habit7.delete_habit_instance() 
    assert Habit.habit_exists(habit7.habit_id, self.db) is False # Ensures habit7 was deleted

    #Add habit that already exists
    habit8 = Habit(name="Clean kitchen cupboards", 
                   description="clean the inside of the kitchen cupboards", 
                   periodicity="weekly", 
                   creation_date="2024-09-18",
                   db=self.db)
    with pytest.raises(ValueError):
      habit8.save()

    #Test __str__ function
    print(habit6.__str__())

    #Test analytics module
    all_habit_data = Habit.get_all_habits(self.db)
    analysis.a1_print_best_perfroming_habit(all_habit_data)
    analysis.a1_print_worst_performing_habit(all_habit_data)
    analysis.a1_print_habits_by_periodicity(all_habit_data, 'daily')
    analysis.a1_print_habits_by_periodicity(all_habit_data, 'weekly')
    analysis.a1_print_habits_by_periodicity(all_habit_data, 'monthly')
    analysis.a1_print_longest_streak(all_habit_data)
    analysis.a1_print_all_habits(all_habit_data)
    
