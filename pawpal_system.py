from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Pet:
    name: str
    type: str
    age: int
    special_needs: str

    def __post_init__(self):
        self.tasks = []  # List of Task objects specific to this pet

    def get_pet_info(self) -> str:
        """Return a string with the pet's information."""
        return f"{self.name} is a {self.age}-year-old {self.type} with special needs: {self.special_needs}"

    def add_task(self, task: Task):
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from the pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self):
        """Return the list of tasks for this pet."""
        return self.tasks

@dataclass
class Task:
    name: str
    duration: int
    priority: str
    category: str
    frequency: str

    def update_priority(self, new_priority: str):
        """Update the task's priority."""
        self.priority = new_priority

    def update_duration(self, new_duration: int):
        """Update the task's duration."""
        self.duration = new_duration

    def get_task_details(self) -> str:
        """Return a string with the task's details."""
        return f"Task: {self.name}, Duration: {self.duration} min, Priority: {self.priority}, Category: {self.category}, Frequency: {self.frequency}"

class PetOwner:
    def __init__(self, name: str, available_time_per_day: int, preferences: str):
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.preferences = preferences
        self.tasks = []
        self.pets = []  # Added: list of Pet objects

    def add_task(self, task: Task):
        """Add a task to the owner's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from the owner's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self):
        """Return the list of tasks for the owner."""
        return self.tasks

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet from the owner's pet list if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self):
        """Return the list of pets for the owner."""
        return self.pets

class Schedule:
    def __init__(self, owner: PetOwner):
        self.owner = owner
        self.tasks = []  # Copy or reference owner's tasks? For now, separate list for scheduled tasks
        self.total_time_used = 0
        self.remaining_time = owner.available_time_per_day

    def get_all_pet_tasks(self):
        """Retrieve all tasks from the owner's pets."""
        return [task for pet in self.owner.pets for task in pet.tasks]

    def add_task(self, task: Task):
        """Add a task to the schedule if it exists in the owner's tasks."""
        if task in self.owner.tasks:
            self.tasks.append(task)
            self.calculate_total_time()

    def remove_task(self, task: Task):
        """Remove a task from the schedule if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)
            self.calculate_total_time()

    def calculate_total_time(self):
        """Calculate total time used and remaining time."""
        self.total_time_used = sum(task.duration for task in self.tasks)
        self.remaining_time = self.owner.available_time_per_day - self.total_time_used

    def display_schedule(self):
        """Print the daily schedule details."""
        print("Daily Schedule:")
        for task in self.tasks:
            print(f"- {task.get_task_details()}")
        print(f"Total time used: {self.total_time_used} min")
        print(f"Remaining time: {self.remaining_time} min")
