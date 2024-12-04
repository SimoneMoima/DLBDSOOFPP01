import sqlite3
from datetime import date, datetime


class HabitDatabase:

    def __init__(self, db_name="main.db"):
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
            self.db.execute("PRAGMA foreign_keys = ON")
            self.create_table()
        except sqlite3.Error as e:
            print(f"Error connecting to the database:{e}")
        
    def create_table(self):
        """Create the habit and tracker tables.
        """
        self.execute_query('''CREATE TABLE IF NOT EXISTS habit (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL, 
                        description TEXT NOT NULL,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT NOT NULL,
                        creation_time TEXT NOT NULL,
                        longest_streak INTEGER DEFAULT 0,
                        current_streak INTEGER DEFAULT 0
                    )''')
        self.execute_query('''CREATE TABLE IF NOT EXISTS tracker (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_id INTEGER,
                        completed_date TEXT,
                        completed_time TEXT,
                        FOREIGN KEY(habit_id) REFERENCES habit(id)
                    )''')
       
    def db_clear_tables(self):
        """Clears all data from habit and tracker tables, and reset id"""
        self.execute_query("DELETE FROM tracker")
        self.execute_query("DELETE FROM habit")
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
        cur = self.execute_query('''INSERT INTO habit (name, description, periodicity, creation_date, creation_time)
                       VALUES (?, ?, ?, ?,?)''', (name, description, periodicity, creation_date, creation_time))
        
        return cur.lastrowid if cur else None
    
    def _db_habit_exists(self, habit_id):
        """Checks if a habit exists

        Args:
            habit_id (int): Internal habit id

        Returns:
            bool: True if habit exists
        """
        cur = self.execute_query("SELECT 1 FROM habit WHERE id = ?", (habit_id,))
        if cur is None:
            print("Query execution failed.")
        result =cur.fetchone()
        return result is not None
    
    def db_delete_habit(self, habit_id):
        """Delete a habit using its ID.

        Args:
            habit_id (int): internal database habit id
        """
        self.execute_query('DELETE FROM tracker WHERE habit_id=?',(habit_id,))
        self.execute_query('DELETE FROM habit WHERE id=?', (habit_id,))
            
    def _db_check_duplicate(self, name, periodicity):
        """Check if a habit with the given name exists in the database.

        Args:
            name (str): Name of the habit to check.

        Returns:
            tuple or None: Returns habit data if a duplicate exists, None otherwise.
        """
       
        cur = self.execute_query("SELECT * FROM habit WHERE name = ? AND periodicity =?", (name, periodicity,))
        return cur.fetchone()  

    def db_get_habit_by_id(self, habit_id):
        """Retrieve habit details by habit_id.

        Args:
            habit_id (int): primary key of habit

        Returns:
           tuple or None: A tuple representing the habit record if found, or else None
        """
        cur = self.execute_query('SELECT * FROM habit WHERE id =?',(habit_id,))
        return cur.fetchone() if cur else None

    def db_get_all_habits(self):
        """Retrieve all habits.

        Returns:
            List[Habit]: returns a list with all database entries for all habits
        """
        cur = self.execute_query('SELECT * FROM habit')
        return cur.fetchall() if cur else None

    def db_update(self, habit_id, name= None, description=None, periodicity=None, longest_streak = None, current_streak = None):
        """Update a habit's description or periodicity.

        Args:
        habit_id (int): The habit ID to update.
        name (str, optional): New name of the habit. Defaults to None.
        description (str, optional): New description. Defaults to None.
        periodicity (str, optional): New periodicity. Defaults to None.
        longest_streak (int, optional): New longest streak. Defaults to None.
        current_streak (int, optional): New current streak. Defaults to None.
        """
        if not habit_id:
            print("Invalid habit id.")
            return 

        cur = self.execute_query('SELECT longest_streak, current_streak FROM habit WHERE id = ?', (habit_id,))
        current_data = cur.fetchone()
        
        if current_data:
            current_longest_streak, current_current_streak = current_data
            if longest_streak is not None and longest_streak != current_longest_streak:
                self.execute_query('''UPDATE habit SET longest_streak=? WHERE id=?''', (longest_streak, habit_id))
            if current_streak is not None and current_streak != current_current_streak:
                self.execute_query('''UPDATE habit SET current_streak=? WHERE id=?''', (current_streak, habit_id))
        if name:
            self.execute_query('''UPDATE habit SET name=? WHERE id=?''', (name, habit_id))
        if description:
            self.execute_query('''UPDATE habit SET description=? WHERE id=?''', (description, habit_id))
        if periodicity:
            self.execute_query('''UPDATE habit SET periodicity=? WHERE id=?''', (periodicity, habit_id))

    def db_record_completion(self, habit_id, completed_date=None, completed_time=None):
        """Mark a habit as completed for a specific date and time.

        Args:
            habit_id (int): _description_
            completed_date (str, optional): _description_. Defaults to None.
            completed_time (str, optional): _description_. Defaults to None.
        """
#        print("inside db-record-completion in habit_database")
        if not self._db_habit_exists(habit_id):
            raise ValueError(f"\n Habit with id {habit_id} does not exists")
        
        if not completed_date:
            completed_date = str(date.today())
        if not completed_time:
            completed_time = str(datetime.now().time().replace(microsecond=0))  # Get current time without microseconds
        
        # Check if theres already a record for the habit on the given date
        cur = self.execute_query(
            'SELECT 1 FROM tracker WHERE habit_id = ? AND completed_date = ?',
            (habit_id, completed_date)
            )
        if cur.fetchone():
            print(f"You already completed the habit with habit id({habit_id}) today.")
            return False 

        self.execute_query('''INSERT INTO tracker (habit_id, completed_date, completed_time)
                    VALUES (?, ?, ?)''', (habit_id, completed_date, completed_time))
            
    def db_get_completed_dates(self, habit_id):
        """Retrieve all completed dates for a habit.

        Args:
            habit_id (int): internal database habit id

        Returns:
          List of completed dates
        """
        if not self._db_habit_exists(habit_id):
            raise ValueError(f"\n Habit with id {habit_id} does not exists")
        
        cur = self.execute_query('SELECT completed_date FROM tracker WHERE habit_id=?', (habit_id,))
        rows = cur.fetchall()
        if not rows:
            print(f"No completed records found for habit_id {habit_id}.")
            return[]
        completed_dates = [row[0] for row in rows]
        return completed_dates

    def db_close(self):
        """Close the database connection
        """
        try:
            if self.db:
                self.db.close()
                self.db =None
                print("Database connection closed")
        except sqlite3.Error as e:
            print(f"Error closing the database: {e}")
