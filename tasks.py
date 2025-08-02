import os
import json
from datetime import date
from typing import List

# ---------- Create Task Objects ---------- #
class Task():
    _id_counter = 0

    def __init__(self, id = None, title = None, description = '', due_date: date = None, status = ''): #Initialise core attributes
        if id is not None: #Unique id per task
            self._id = id
        else:
            self._id = Task._gen_id()

        self._title = title  #Short description
        self._description = description  #Details
        self._due_date = due_date  #Due date (optional)
        self._status = status  #Pending or Complete

    def __str__(self):  #For readability
        return f"Task #{self._id}: {self._title} [{self._status}]"

    # ---------- Getters ---------- #
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def due_date(self):
        return self._due_date

    @property
    def priority(self):
        if self._due_date is not None:
            days_left = (self._due_date - date.today()).days
            if days_left <= 2:
                return 1  # High
            elif 2 < days_left < 7:
                return 2  # Medium
            else:
                return 3  # Low
        else:
            return 4

    @property
    def status(self):
        return self._status

    # ---------- Helper Methods ---------- #

    def mark_complete(self):  #Change status to complete
        self._status = 'complete'

    def mark_incomplete(self):  #Change status to incomplete
        self._status = 'pending'

    def toggle_status(self):  #Flip status
        if self._status == 'complete':
            self._status = 'pending'
            return
        elif self._status == 'pending':
            self._status = 'complete'
            return

    def update_title(self, new_title):  #Update title
        self._title = new_title

    def update_description(self, new_description):  #Update description
        self._description = new_description

    def set_due_date(self, date_str: str):  #Fiddle with this and maybe a calendar widget later? Take in a date as a list [YYYY, MM, DD]
        self._due_date = date.fromisoformat(date_str)

    def is_overdue(self):  #Check if the task is already past its deadline, if it exists
        if self._due_date is None:
            return False
        else:
            return self._due_date < date.today()

    def to_dict(self) -> dict:  #Convert object into a dictionary for json processing
        task = {'id': self._id, 'title': self._title, 'description': self._description, 'due date': self._due_date.isoformat() if self._due_date else None, 'status': self._status}
        return task

    # ---------- Utility methods ---------- #
    @classmethod
    def from_dict(cls, task: dict):  #Create task object from a dictionary
        date_str = task.get('due date')
        due = date.fromisoformat(date_str) if date_str else None

        return cls(id = task['id'], title = task['title'], description = task['description'],
                   due_date = due, status = task['status'])

    @classmethod
    def _gen_id(cls):  #Initialise an ID for the task object
        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def set_id_counter(cls, new_id_count: int): #Set the id counter to the max of the existing task list
        cls._id_counter = new_id_count

    @classmethod
    def get_max_id(cls):
        return cls._id_counter


# ---------- JSON Management ---------- #

def load_tasks():  # Load list of tasks from json file
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasklist: List[dict]):  # Save list of tasks to json file
    with open('tasks.json', 'w') as file:
        json.dump(tasklist, indent=2)

# ---------- Create the manager ---------- #
class TaskManager():

    # ---------- Initialisation ---------- #
    def __init__(self, tasklist: List[dict] = None): #Initialise list of Task objects for the manager
        if tasklist:
            self._tasks = [Task.from_dict(task) for task in tasklist]
        else:
            self._tasks = []

    # ---------- Helper Methods ---------- #
    def sync_id_count(self, tasks: List[Task]):  #Sync the highest id number of the loaded list
        if self._tasks:
            Task.set_id_counter(max(task.id for task in tasks))

    def check_empty(self):  #Check if the task list is currently empty
        if len(self._tasks) == 0:
            return True
        else:
            return False

    # ---------- Manager functionality ---------- #

    def add_task(self, new_task: Task):  #Add a new task to keep track of
        if isinstance(new_task, Task):
            self._tasks.append(new_task)
            task_dict_list = [task.to_dict() for task in self._tasks]
            save_tasks(task_dict_list)
        else:
            raise TypeError("Expected a Task instance.")

    def del_task(self, existing_task: Task):  #Remove a task from the list
        if self.check_empty():
            return "The task list is currently empty."
        if isinstance(existing_task, Task):
            self._tasks.remove(existing_task)
            task_dict_list = [task.to_dict() for task in self._tasks]
            save_tasks(task_dict_list)
        else:
            raise TypeError("Expected a Task instance.")

    def update_task(self, new_task: Task, existing_id: int = None, existing_title: str = None):  #Update a task with corresponding ID or title with a new task
        if self.check_empty():
            return "The task list is currently empty."
        if isinstance(new_task, Task):
            for index, task in enumerate(self._tasks):
                if (existing_id is not None and task.id == existing_id) or (existing_title is not None and task.title == existing_title):
                    self._tasks[index] = new_task
                    save_tasks([t.to_dict() for t in self._tasks])
                    break
            else:
                raise ValueError("No task with the given id or title currently exists.")
        else:
            raise TypeError("Expected a Task instance.")

    def get_tasks(self):  #Retrieve all tasks tracked by the manager
        if self.check_empty():
            return "The task list is currently empty."
        return self._tasks

    def get_task_by_id(self, id_num: int = None):  #Retrieve a specific task by ID
        if self.check_empty():
            return "The task list is currently empty."
        if id_num is not None and 0 < id_num <= Task.get_max_id():
            for task in self._tasks:
                if task.id == id_num:
                    return task
            else:
                raise ValueError("No task with the given id currently exists.")
        else:
            raise ValueError("Expected a valid task id.")

    def get_task_by_status(self, status: str = None):  #Retrieve a list of tasks with the corresponding status
        if self.check_empty():
            return "The task list is currently empty."
        filtered_tasks = []
        if status is not None and status.lower() in ['pending', 'complete']:
            for task in self._tasks:
                if task.status == status:
                    filtered_tasks.append(task)
        else:
            raise ValueError("Expected a valid status.")

        return filtered_tasks

    def sort_tasks_by_priority(self) -> List[Task]:  #Sort tasks by priority first, then ID
        return sorted(self._tasks, key = lambda task_item: (task_item.priority, task_item.id))

