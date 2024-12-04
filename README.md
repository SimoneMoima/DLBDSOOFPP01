# Habit Tracking Application

This application is a habit tracker. You can add, update, track and analyse daily or weekly habits. 

## What is it
Please make sure you have the Python installed on your computer. 
Start the Application by pulling the code from the git repository to you development platform and follow the installation guide.
The application uses sqlite3 to store the data and pytest for testing. Tests are prewritten and stored in the test_project.py file. 
Otherwise a CLI can be used to navigate the application (click). More information in 'Usage'.

## Installation
Install python
1. Clone the repository:
    ```bash
    git clone https://github.com/SimoneMoima/Habit-Tracker.git
    ```
2. Navigate to project directory:
    ```bash
    cd PythonProject
    ```
3. Install the dependencies:
    ```shell
    pip install -r requirements.txt
    ```

## Usage

Start

```shell
python cli.py main-menu
```
and follow instructions on screen.

## Tests

```shell
pytest .
```