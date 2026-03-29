from pawpal_system import PetOwner, Pet, Task, Schedule

# Create an owner
owner = PetOwner("Alice", 480, "Prefers morning routines")  # 480 minutes = 8 hours available

# Create at least two pets
pet1 = Pet("Buddy", "Dog", 3, "Needs daily medication")
pet2 = Pet("Whiskers", "Cat", 2, "Special diet required")

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create at least three tasks with different durations
task1 = Task("Morning Walk", 30, "high", "exercise", "daily")  # 30 minutes
task2 = Task("Feeding", 15, "medium", "feeding", "daily")     # 15 minutes
task3 = Task("Playtime", 45, "low", "play", "daily")          # 45 minutes

# Add tasks to pets
pet1.add_task(task1)  # Buddy gets the walk
pet1.add_task(task2)  # Buddy gets feeding
pet2.add_task(task3)  # Whiskers gets playtime


# Create a schedule and show all pet tasks
schedule = Schedule(owner)
all_tasks = schedule.get_all_pet_tasks()
print(f"\nAll tasks from owner's pets: {[task.name for task in all_tasks]}")
