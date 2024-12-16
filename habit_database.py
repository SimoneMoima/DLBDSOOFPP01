import sqlite3
from datetime import date, datetime


class HabitDatabase:

    def __init__(self, db_name="main.db"):
        """Initialize the database"""
        self.db_name = db_name
        self.db = None
        self.connect()

    def execute_query(self, query, params=()):
        """Execute a database query

        Args:
            query (str): Intendet SQL Query to the database
            params (tuple, optional): parameters that are used with the query. Defaults to ().
        """
        try:
            cur = self.db.cursor()
            cur.execute(query, params)
            self.db.commit()
            return cur
        except sqlite3.Error as e:
            print(f"Error executing query: {query}. Error {e}")
            self.db.rollback()
            return None
        
    def connect(self):
        """Connect to the database and initialize tables.
        """
        try:
            self.db = sqlite3.connect(self.db_name)
            self.db.execute("PRAGMA foreign_keys = ON")  #Enforce referential integrity
            self.create_table()
        except sqlite3.Error as e:
            print(f"Error connecting to the database:{e}")
        
    def create_table(self):
        """Create the habit and tracker tables.
        """
        self.execute_query(
            '''CREATE TABLE IF NOT EXISTS habit (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL, 
                        description TEXT NOT NULL,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT NOT NULL,
                        creation_time TEXT NOT NULL,
                        longest_streak INTEGER DEFAULT 0,
                        current_streak INTEGER DEFAULT 0
                        )'''
            )
        self.execute_query(
            '''CREATE TABLE IF NOT EXISTS tracker (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_id INTEGER,
                        completed_date TEXT,
                        completed_time TEXT,
                        FOREIGN KEY(habit_id) REFERENCES habit(id)
                        )'''
            )
       
    def db_clear_tables(self):
        """Clears all data from habit and tracker tables, and reset id"""
        self.execute_query('DELETE FROM tracker')
        self.execute_query('DELETE FROM habit')
        self.execute_query("UPDATE sqlite_sequence SET seq=0 WHERE name='habit'")
        self.execute_query("UPDATE sqlite_sequence SET seq=0 WHERE name='tracker'")
        
    def db_save(self, name, description, periodicity, creation_date, creation_time):
        """Insert a new habit into the habit table.

        Args:
            name (str): name of habit
            description (str): description of habit
            periodicity (str): periodicity of habit
            creation_date (str): creation date
            creation_time (str): creation time

        Returns:
            habit_id(int): returns the primary key (id) of the created habit.
        """
        cur = self.execute_query(
            '''INSERT INTO habit (name, description, periodicity, creation_date, creation_time)
                VALUES (?, ?, ?, ?,?)''', 
            (name, description, periodicity, creation_date, creation_time)
        )
        
        return cur.lastrowid 
    
    def db_habit_exists(self, habit_id):
        """Checks if a habit exists

        Args:
            habit_id (int): Internal habit id

        Returns:
            bool: True if habit exists. False otherwise
        """
        cur = self.execute_query(
            "SELECT 1 FROM habit WHERE id = ?", 
            (habit_id,)
            )
        
        result = cur.fetchone()

        if result is None:
            return False

        return result 
    
    def db_delete_habit(self, habit_id):
        """Delete a habit using its ID.

        Args:
            habit_id (int): internal database habit id
        """
        self.execute_query(
            'DELETE FROM tracker WHERE habit_id=?',
            (habit_id,)
            )
        self.execute_query(
            'DELETE FROM habit WHERE id=?', 
            (habit_id,)
            )
            
    def db_check_duplicate(self, name, periodicity):
        """Check if a habit with the given name exists in the database.

        Args:
            name (str): Name of the habit to check.

        Returns:
            tuple or None: Returns habit data if a duplicate exists, None otherwise.
        """
       
        cur = self.execute_query(
            'SELECT * FROM habit WHERE name = ? AND periodicity =?', 
            (name, periodicity,)
            )
        return cur.fetchone()  

    def db_get_habit_by_id(self, habit_id):
        """Retrieve habit details by habit_id.

        Args:
            habit_id (int): primary key of habit

        Returns:
           tuple or None: A tuple representing the habit record if found, or else None
        """
        # Check if habit exists by id
        if not self.db_habit_exists(habit_id):
            raise ValueError(f"\n Habit with id {habit_id} does not exists")
        
        #SQL qery to get the habits information
        cur = self.execute_query(
            'SELECT * FROM habit WHERE id =?',
            (habit_id,)
            )
        
        return cur.fetchone() 

    def db_get_all_habits(self):
        """Retrieve all habits.

        Returns:
            List[Habit]: returns a list with all informaion for all habits
        """
        #SQL query to get all habit data
        cur = self.execute_query('SELECT * FROM habit')
        
        #return if there are no habits
        if not cur: 
            print("No habits found in the database.")
            return []
        
        all_habits = cur.fetchall()

        return all_habits

    def db_update(self, habit_id, name= None, description=None, periodicity=None):
        """Update a habit's description or periodicity.

        Args:
        habit_id (int): The habit ID to update.
        name (str, optional): New name of the habit. Defaults to None.
        description (str, optional): New description. Defaults to None.
        periodicity (str, optional): New periodicity. Defaults to None.
        """
        # Check if habit exists
        if not self.db_habit_exists(habit_id):
            print("Invalid habit id.")
            return 
        
        if name: # Update habit name
            self.execute_query(
                'UPDATE habit SET name=? WHERE id=?', 
                (name, habit_id)
                )
        if description: # Update habit description
            self.execute_query(
                'UPDATE habit SET description=? WHERE id=?', 
                (description, habit_id)
                )
        if periodicity: # Update habit periodicity
            self.execute_query(
                'UPDATE habit SET periodicity=? WHERE id=?', 
                (periodicity, habit_id)
                )
    
    def db_update_streak(self, habit_id, current_streak: int = None, longest_streak: int = None):
        """Updates the streak data in the database (current and longest)

        Args:
            habit_id (int): habit id of completed habit
            current_streak (int, optional): Current streak of a habit. Defaults to None.
            longest_streak (int, optional): longest streak of a habit. Defaults to None.
        """
        # get current streak data
        cur = self.execute_query(
            'SELECT longest_streak, current_streak FROM habit WHERE id = ?', 
            (habit_id,)
            )
        current_data = cur.fetchone()
        #Check if streak data is not equal or empty, then update 
        if current_data:
            current_longest_streak, current_current_streak = current_data
            if longest_streak is not None and longest_streak != current_longest_streak:
                self.execute_query(
                    'UPDATE habit SET longest_streak=? WHERE id=?', 
                    (longest_streak, habit_id)
                    )
            if current_streak is not None and current_streak != current_current_streak:
                self.execute_query(
                    'UPDATE habit SET current_streak=? WHERE id=?', 
                    (current_streak, habit_id)
                    )

    def db_already_marked_completed(self,name, habit_id, completed_date):
        """check if a habit was already marked completed on a given day.

        Args:
            name (str): _name of habit
            habit_id (int): habit id
            completed_date (str): completion date

        Returns:
            bool: True if the habit already exists and False otherwise
        """
        cur = self.execute_query(
                'SELECT 1 FROM tracker WHERE habit_id = ? AND completed_date = ?',
                (habit_id, completed_date)
               )
        result = cur.fetchone()
        if result and result[0] == 1:
            print(f"\nHabit {habit_id} - '{name}' has already been marked completed today.")
            return True
        
        return False

    def db_record_completion(self, name, habit_id, completed_date: str = None, completed_time: str = None):
        """Mark a habit as completed for a specific date and time.

        Args:
            habit_id (int): _description_
            completed_date (str, optional): _description_. Defaults to None.
            completed_time (str, optional): _description_. Defaults to None.
        Raises:
            Value Error: Habit doesnt exist
        """
        # check if habit exists by id
        if not self.db_habit_exists(habit_id):
            raise ValueError(f"\n Habit with id {habit_id} does not exists")

        # If date and time are not given, save current date and time
        if completed_date is None:
            completed_date = str(date.today())
        if completed_time is None:
            completed_time = str(datetime.now().time().replace(microsecond=0))  # Get current time without microseconds
        
        #check if habit was marked completed already on the day
        result = self.db_already_marked_completed(name, habit_id, completed_date)
 
        if not result:
            self.execute_query(
            '''INSERT INTO tracker (habit_id, completed_date, completed_time)
                VALUES (?, ?, ?)''', 
                (habit_id, completed_date, completed_time)
            )
            print(f"\n-----Habit {habit_id} - '{name}' was completed on {completed_date} at {completed_time}----\n")
            
    def db_get_completed_dates(self, habit_id):
        """Retrieve all completed dates for a habit.

        Args:
            habit_id (int): internal database habit id

        Returns:
           List [str]: List of completed dates
        
        Raises: 
            Value Error: Habit doesnt exist.
        """
        # Check if habit exists by id
        if not self.db_habit_exists(habit_id):
            raise ValueError(f"\n Habit with id {habit_id} does not exists")
        
        # SQL query to get all the completed dates from the given habit by id
        cur = self.execute_query(
            '''SELECT completed_date FROM tracker WHERE habit_id=?''', 
            (habit_id,)
            )
        rows = cur.fetchall()
        # Return if the habit has not been completed yet.
        if not rows:
            print(f"No completed records found for habit_id {habit_id}.")
            return[]
        # Save all retrieved dates in a list and return it
        completed_dates = [row[0] for row in rows]
        return completed_dates

    def db_close(self):
        """Close the database connection
        """
        try:
            if self.db:
                self.db.close()
                self.db =None # Reset to default
                print("Database connection closed")
        except sqlite3.Error as e:
            print(f"Error closing the database: {e}")
