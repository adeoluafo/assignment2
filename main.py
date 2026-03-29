from pawpal_system import PetOwner, Pet, Task, Schedule
from datetime import datetime

# Create an owner
owner = PetOwner("Alice", 480, "Prefers morning routines")  # 480 minutes = 8 hours available

# Create at least two pets
pet1 = Pet("Buddy", "Dog", 3, "Needs daily medication")
pet2 = Pet("Whiskers", "Cat", 2, "Special diet required")

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create at least three tasks with different durations
task1 = Task("Morning Walk", 30, "high", "exercise", "daily", "08:00", "pending", "Buddy", datetime.now())
task2 = Task("Feeding", 15, "medium", "feeding", "daily", "12:00", "completed", "Buddy", datetime.now())
task3 = Task("Playtime", 45, "low", "play", "daily", "18:00", "pending", "Whiskers", datetime.now())

# Add more tasks out of chronological order
task4 = Task("Evening Walk", 25, "medium", "exercise", "daily", "19:30", "pending", "Buddy", datetime.now())
task5 = Task("Medication", 5, "high", "medication", "daily", "09:00", "completed", "Buddy", datetime.now())
task6 = Task("Grooming", 60, "low", "grooming", "weekly", "14:00", "pending", "Whiskers", datetime.now())
task7 = Task("Vet Check", 30, "high", "health", "monthly", "10:00", "pending", "Buddy", datetime.now())
task8 = Task("Brushing", 20, "medium", "grooming", "daily", "08:00", "pending", "Buddy", datetime.now())  # Same time as Morning Walk!

# Add tasks to pets out of order (not in creation sequence)
pet1.add_task(task5)  # Buddy gets medication first
pet2.add_task(task3)  # Whiskers gets playtime
pet1.add_task(task1)  # Buddy gets the walk
pet1.add_task(task7)  # Buddy gets vet check
pet2.add_task(task6)  # Whiskers gets grooming
pet1.add_task(task4)  # Buddy gets evening walk
pet1.add_task(task2)  # Buddy gets feeding last
pet1.add_task(task8)  # Buddy gets brushing (same time as morning walk!)


# Create a schedule and show all pet tasks
schedule = Schedule(owner)
all_tasks = schedule.get_all_pet_tasks()
print(f"\nAll tasks from owner's pets: {[task.name for task in all_tasks]}")

# Sort tasks by time
sorted_tasks = schedule.sort_by_time()
print(f"\nTasks sorted by time: {[f'{task.name} at {task.time}' for task in sorted_tasks]}")

# Filter tasks by completion status
pending_tasks = schedule.filter_tasks(completion_status="pending")
print(f"\nPending tasks: {[task.name for task in pending_tasks]}")

completed_tasks = schedule.filter_tasks(completion_status="completed")
print(f"Completed tasks: {[task.name for task in completed_tasks]}")

# Filter tasks by pet name
buddy_tasks = schedule.filter_tasks(pet_name="Buddy")
print(f"\nBuddy's tasks: {[task.name for task in buddy_tasks]}")

whiskers_tasks = schedule.filter_tasks(pet_name="Whiskers")
print(f"Whiskers' tasks: {[task.name for task in whiskers_tasks]}")

# Filter by both status and pet name
buddy_pending = schedule.filter_tasks(completion_status="pending", pet_name="Buddy")
print(f"\nBuddy's pending tasks: {[task.name for task in buddy_pending]}")

whiskers_pending = schedule.filter_tasks(completion_status="pending", pet_name="Whiskers")
print(f"Whiskers' pending tasks: {[task.name for task in whiskers_pending]}")

# Demonstrate recurring task functionality
print(f"\n--- Demonstrating Recurring Tasks ---")
print(f"Total tasks before marking complete: {len(schedule.get_all_pet_tasks())}")

# Mark the "Feeding" task as complete (it's daily, so should create a new one)
feeding_task = None
for task in schedule.get_all_pet_tasks():
    if task.name == "Feeding" and task.pet_name == "Buddy":
        feeding_task = task
        break

if feeding_task:
    print(f"Marking '{feeding_task.name}' as complete...")
    schedule.mark_task_complete(feeding_task)
    
    print(f"Total tasks after marking complete: {len(schedule.get_all_pet_tasks())}")
    
    # Show all tasks again with due dates
    all_tasks_after = schedule.get_all_pet_tasks()
    print("All tasks after completion:")
    for task in all_tasks_after:
        due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
        print(f"  - {task.name} ({task.completion_status}) - Due: {due_date_str}")
    
    # Show pending tasks
    pending_after = schedule.filter_tasks(completion_status="pending")
    print(f"Pending tasks after completion: {[task.name for task in pending_after]}")

# Demonstrate conflict detection
print(f"\n--- Demonstrating Conflict Detection ---")
conflicts = schedule.detect_time_conflicts()
if conflicts:
    print("⚠️  SCHEDULE CONFLICTS DETECTED:")
    for warning in conflicts:
        print(f"   {warning}")
else:
    print("✅ No time conflicts detected in the schedule.")
