
from habit_database import HabitDatabase
from datetime import date, datetime, timedelta

class Habit:

    def __init__(self, 
                 name: str, 
                 description: str, 
                 periodicity: str, 
                 creation_date: str = None, 
                 creation_time: str = None, 
                 db = None
        ):
        """Habit class to store habits

        Args:
            name (str): Name of the habit. 
            description (str): Short description of the habit. 
            periodicity (str): daily, weekly. 
            creation_date (str): date the habit was created. Defaults to current date
            creation_time (str): time the habit was created. Defaults to current time
            db (object, optional): Database connection or interface. Defaults to a new HabitDatabaase instance.
        """
        self.db = db if db else HabitDatabase()
        self.habit_id = None
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date or str(date.today())
        self.creation_time = creation_time or str(datetime.now().time().replace(microsecond=0))
        self.longest_streak: int = 0
        self.current_streak: int = 0

    def clear_table(self):
        """Clears all entries in the habit and tracker tables and sets all ids to 0.
        """
        self.db.db_clear_tables()

    def delete_habit(self):
        """Deletes the habit
        """
        self.db.db_delete_habit(self.habit_id)
    
    def _correct_periodicity(self, periodicity: str):
        """Checks if the correct periodicity is entered

        Args:
            periodicity (str): periodicity that needs to be evaluates

        Raises:
            ValueError: Wrong periodicity entered. Must be daily or weekly
        """
        valid_periodicities={'daily', 'weekly', 'monthly'}
        if periodicity not in valid_periodicities:
            raise ValueError(f"Invalid periodicity: {periodicity}. Must be {valid_periodicities}")
          
    def __str__(self):
        """Returns a string of all habit data for printout

        Returns:
            str: string with all habit data
        """
        return ( "\nHabit information: \n"
                "--------------------------------\n"
                f"Habit ID: {self.habit_id}\n"
                f"Habit: {self.name}\n"
                f"Description: {self.description}\n"
                f"Periodicity: {self.periodicity}\n"
                f"Creation Date: {self.creation_date}\n"
                f"Creation Time: {self.creation_time}\n"
                f"Current streak: {self.current_streak}\n"
                f"Longest streak: {self.longest_streak}\n"
                "--------------------------------\n"
        )
    
    @classmethod
    def is_duplicate(self, name: str, periodicity: str, db = None):
        """Check for duplicates of habit names in database
            Returns bool: True if duplicate exitsts
        """
        db = db if db else HabitDatabase()  # Initialize database connection
        duplicate = db.db_check_duplicate(name, periodicity)
        
        if duplicate:
            return True
        return False
    
    @classmethod
    def habit_exists(self, habit_id: int, db=None):
        """checks if habit exists

        Returns:
            bool: true if habit exists
        """
        db = db if db else HabitDatabase()  # Initialize database connection

        habit_exists = db.db_habit_exists(habit_id)
        return habit_exists

    def save(self):
        """Save the habit in the database, current date and time are automatically added

        Args:
            db (_type_, optional): _description_. Defaults to None.

        Raises:
            ValueError: Habit name is empty or longer than 255 char
            ValueError: Habit with the name already exists.
        """
        if not self.name or len(self.name) > 255:
            raise ValueError("Habit name must be non empty and less than 255 char.")
        
        # Check if periodicity is correct 
        self._correct_periodicity(self.periodicity)

        # Check if name and periodicity pair does not exist already
        
        if self.db.db_check_duplicate(self.name, self.periodicity):
            raise ValueError(f"A habit with the name '{self.name}' and periodicity '{self.periodicity}' already exists.")
            
        self.habit_id = self.db.db_save(self.name, self.description, self.periodicity, self.creation_date, self.creation_time)
       
        
    def update(self, name=None, description=None, periodicity=None):
        """
        Update habit attributes in the database

        Args:
            name (str): Name of the  habit. Defaults to None.
            description (str): Description of habit. Defaults to None.
            periodicity (str): Periodicity of habit. Defaults to None.
        """
        if name: # Set new habit name
            self.is_duplicate(name, periodicity) # Check if habit with this name and periodicity already exists
            self.name = name
        if description: # Set new habit description
            self.description = description
        if periodicity: # Set new habit periodicity 
            self.periodicity = periodicity
            self._correct_periodicity(self.periodicity) # Check if periodicity was entered correctly
        if self.habit_id: # Call update function 
            self.db.db_update(self.habit_id, name=name, description=description, periodicity=periodicity)
    @staticmethod
    def correct_date_format(completed_date: str):
        try:
            datetime.strptime(completed_date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    @staticmethod
    def correct_time_format(completed_time: str):
         try:
            datetime.strptime(completed_time, "%H:%M:%S")
            return True
         except ValueError:
             return False
         
    def zero_pad_date(self, completed_date):
        """Ensures dates are saved in the correct format with zero padding

        Args:
            completed_date (str): completion date

        Raises:
            ValueError: String doesnt have the correct format

        Returns:
            str: date string with zero padding
        """
        try:
            year, month, day = map(int,completed_date.split("-"))
            return f"{year:04d}-{month:02d}-{day:02d}"
        except ValueError:
            raise ValueError("\nInput date string must be in 'YYYY-M-D' format.")
        
    def record_completion(self, completed_date: str = None, completed_time: str = None):
        """Marks a habit as completed 

        Args:
            completed_date (str, optional): Date of completion. Defaults to None.
            completed_time (str, optional): Time of completion. Defaults to None.

        Raises:
            ValueError: Habit has not been saved to database no id was set
        """
        #If date and time are empty, use current date and time
        if completed_date is None:
            completed_date = str(date.today())
        else:
            completed_date = self.zero_pad_date(completed_date)
        if completed_time is None:
            completed_time = str(datetime.now().time().replace(microsecond=0))
       
        #Ensure habit_id is set
        if not self.habit_id:
            raise ValueError("\nHabit must be saved before completed")
        
        self.db.db_record_completion(self.name, self.habit_id, completed_date, completed_time)

        #Automatically calculate and save streak data
        if self.periodicity == 'daily':
            self.calculate_daily_streak()
        elif self.periodicity == 'weekly':
            self.calculate_weekly_streak()
        elif self.periodicity == 'monthly':
            self.calculate_monthly_streak()

    def _get_completed_dates(self):
        """Retrieve all completion dates for the habit by internal id

        Returns:
            List: list of all completed dates for a habit
        """
        return self.db.db_get_completed_dates(self.habit_id)
    
    def get_habit_by_id(self):
        """Gets a habit by id
        """
        self.db.db_get_habit_by_id(self.habit_id)

    @classmethod
    def get_by_id(cls, habit_id, db=None):
        """Retrieve a habit by its ID

        Args:
            habit_id (int): internal database id of a habit
            db (_type_, optional): _description_. Defaults to None.

        Raises:
            ValueError: Habit id does not exist

        Returns:
            List: List with all habit values as enties
        """
        db = db if db else HabitDatabase() # Initialize database connection
        #Check if habit exists
        if not db.db_habit_exists:
            return
        # Fetch habit data
        habit_data = db.db_get_habit_by_id(habit_id)
        # Save habit data in a List
        habit = cls( 
            name = habit_data[1],
            description = habit_data[2],
            periodicity = habit_data[3]
            )
        habit.habit_id = habit_data[0]
        habit.creation_date = habit_data[4]  
        habit.creation_time = habit_data[5]  
        habit.longest_streak = habit_data[6]
        habit.current_streak = habit_data[7]
        return habit
    
    @classmethod
    def get_all_habits(cls, db=None):
        """Class method to retrieve all habits with creation date and longest streak.

        Args:
            db (_type_, optional): _Can be used to save in alternative db. Defaults to None.

        Returns:
            List [Habits]: List of all current habits
        """
        db = db if db else HabitDatabase()  # Initialize database connection
        all_habit_data = db.db_get_all_habits()  # Retrieve all habits data
        
        # Create Habit instances for each habit record
        all_habits = []
        try:
            for data in all_habit_data:
                habit = cls(
                    name=data[1], 
                    description=data[2], 
                    periodicity=data[3],
                )
                habit.habit_id = data[0]
                habit.creation_date = data[4] 
                habit.creation_time = data[5] 
                habit.longest_streak = data[6] 
                habit.current_streak = data[7]
                all_habits.append(habit)
        except Exception as  e:
            raise RuntimeError(f"\nFailed to retrieve all habits: {e}")
        
        return all_habits
    
    def _update_current_streak(self,streak):
        """Updates the current streak variable in the database

        Args:
            streak (int): length of current streak
        """
        self.current_streak = streak
        self.db.db_update_streak(habit_id=self.habit_id, current_streak = streak)
        
    def _update_longest_streak(self, streak):
        """Updates the longest streak variable to current streak if it is longer than previouse one

        Args:
            streak (int): longest ever streak
        """
        if streak > self.longest_streak:
            self.longest_streak = streak
            self.db.db_update_streak(habit_id=self.habit_id,longest_streak=self.longest_streak)
    
    def calculate_daily_streak(self):
        """Calculate the daily streak of consecutive completions.
        """
        completed_dates = self._get_completed_dates()
        #Sort the List to make sure the most recent date is evaluated first
        completed_dates = sorted(
            {datetime.strptime(date_str, "%Y-%m-%d").date() for date_str in completed_dates}, 
            reverse=True
        )

        streak = 0
        today = date.today()

        #calculate the daily streak
        for completed_date in completed_dates:
            if today == completed_date:
                streak += 1
                today -= timedelta(days=1)  # Move to the previous day
            else:
                break  # Streak is broken if there’s a gap
        
        self._update_longest_streak(streak)
        self._update_current_streak(streak)
     
    def _get_mondays(self,day: date):
        """Helper function to get the start of the week for a given date.
        Args:
             day(datetime.date()): given date
        Retruns: 
             datetime.day(): Monday of the week of the day that was given
        """
        # The day.weekday() function returns the given weekday as an integer (Wednesday = 2)
        # Timedelta creates a time duration of the returned integer (timedelta = 2 days) and
        # subtracts it from the given day.
        # This will always return the Monday of the week.
        return day - timedelta(days=day.weekday())

    def calculate_weekly_streak(self):
        """Calculate the current weekly streak of consecutive weeks for a habit.

        Returns:
            int: length of streak
        """

        completed_dates = self._get_completed_dates() # get completed dates from the database
        mondays = sorted(
            {self._get_mondays(datetime.strptime(date, "%Y-%m-%d").date()) for date in completed_dates},
            reverse=True
        ) # Sorted Set of all unique Mondays of the weeks where the habit was completed, this enables an algorithm to check for weekly entries

        # If no unique week starts, return 0 streak
        if not mondays:
            return 0

        streak = 0
        current_monday = self._get_mondays(date.today())

        # Calculate streak by checking consecutive weeks in the sorted list
        for monday in mondays:
            if current_monday == monday:
                streak += 1
                current_monday -= timedelta(weeks = 1)  #subtract a week and set for next comparison
            else:
                break  # Streak is broken if there’s a gap

        self._update_longest_streak(streak)
        self._update_current_streak(streak)
        return streak
     
    def calculate_monthly_streak(self):
        """Function to calculate monthly streaks

        Returns:
            int: calculated streak
        """
        streak = 0
        previous = None

        completed_dates = self._get_completed_dates()

        if not completed_dates:
            print("You have not completed this habit yet.")
            return

        years_months = sorted({(datetime.strptime(date, "%Y-%m-%d").year, datetime.strptime(date, "%Y-%m-%d").month) for date in completed_dates}, 
              reverse= True ) # Set of sorted and unique (year, month) pairs
        
        
        for year, month in years_months:
            # In first iteration, previous is None. Then year and month of the first entry are added
            # Check if next month is contained, or check if there was a change in year -> add to streak else leave for loop
            if previous is None:
                streak += 1
                previous= (year, month)
            else: 
                if (year == previous[0] and month == previous[1] - 1) or (year == previous[0] - 1 and month == 12 and previous[1] == 1):
                    streak += 1
                    previous = (year, month) # Update year and month
                else:
                    break # Streak is broken if there is a gap
        
        self._update_current_streak(streak)
        self._update_longest_streak(streak)

        return streak




    