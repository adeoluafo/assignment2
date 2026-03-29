from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta

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
    time: str = "00:00"  # HH:MM format
    completion_status: str = "pending"  # "pending", "completed", "in_progress"
    pet_name: str = ""  # Name of the pet this task belongs to
    due_date: datetime = None  # Due date for the task

    def update_priority(self, new_priority: str):
        """Update the task's priority."""
        self.priority = new_priority

    def update_duration(self, new_duration: int):
        """Update the task's duration."""
        self.duration = new_duration

    def update_completion_status(self, new_status: str):
        """Update the task's completion status."""
        if new_status in ["pending", "completed", "in_progress"]:
            self.completion_status = new_status
        else:
            raise ValueError("Invalid status. Must be 'pending', 'completed', or 'in_progress'")

    def create_recurring_task(self):
        """Create a new instance of this task for the next occurrence if it's recurring."""
        if self.frequency.lower() in ["daily", "weekly"] and self.completion_status == "completed":
            # Calculate next due date
            if self.due_date is None:
                self.due_date = datetime.now()
            
            if self.frequency.lower() == "daily":
                next_due_date = self.due_date + timedelta(days=1)
            elif self.frequency.lower() == "weekly":
                next_due_date = self.due_date + timedelta(weeks=1)
            
            # Create new task with same properties but reset status and updated due date
            new_task = Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                category=self.category,
                frequency=self.frequency,
                time=self.time,
                completion_status="pending",
                pet_name=self.pet_name,
                due_date=next_due_date
            )
            return new_task
        return None

    def get_task_details(self) -> str:
        """Return a string with the task's details."""
        due_date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else "None"
        return f"Task: {self.name}, Duration: {self.duration} min, Priority: {self.priority}, Category: {self.category}, Frequency: {self.frequency}, Time: {self.time}, Status: {self.completion_status}, Pet: {self.pet_name}, Due: {due_date_str}"

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

    def sort_by_time(self):
        """Sort and return all pet tasks by time (earliest to latest)."""
        def time_to_minutes(t):
            h, m = map(int, t.split(':'))
            return h * 60 + m
        return sorted(self.get_all_pet_tasks(), key=lambda task: time_to_minutes(task.time))

    def filter_tasks(self, completion_status: str = None, pet_name: str = None):
        """Filter tasks by completion status and/or pet name.
        
        Args:
            completion_status: Filter by status ("pending", "completed", "in_progress")
            pet_name: Filter by pet name
            
        Returns:
            List of filtered tasks
        """
        tasks = self.get_all_pet_tasks()
        
        if completion_status:
            tasks = [task for task in tasks if task.completion_status == completion_status]
        
        if pet_name:
            tasks = [task for task in tasks if task.pet_name == pet_name]
            
        return tasks

    def mark_task_complete(self, task: Task):
        """Mark a task as completed and create recurring task if applicable."""
        task.update_completion_status("completed")
        
        # Create new recurring task if applicable
        new_task = task.create_recurring_task()
        if new_task:
            # Find the pet and add the new task
            for pet in self.owner.pets:
                if pet.name == task.pet_name:
                    pet.add_task(new_task)
                    break

    def detect_time_conflicts(self):
        """Detect and return warnings for tasks scheduled at the same time.
        
        Returns:
            List of warning messages for conflicting tasks
        """
        warnings = []
        tasks = self.get_all_pet_tasks()
        
        # Group tasks by time
        time_groups = {}
        for task in tasks:
            if task.time not in time_groups:
                time_groups[task.time] = []
            time_groups[task.time].append(task)
        
        # Check for conflicts
        for time_slot, task_list in time_groups.items():
            if len(task_list) > 1:
                task_names = [f"{task.name} ({task.pet_name})" for task in task_list]
                warning = f"⚠️  TIME CONFLICT at {time_slot}: {', '.join(task_names)} are scheduled simultaneously"
                warnings.append(warning)
        
        return warnings

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
