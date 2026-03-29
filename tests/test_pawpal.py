import unittest
from pawpal_system import PetOwner, Pet, Task, Schedule

class TestPawPal(unittest.TestCase):

    def test_pet_add_task(self):
        """Test that a task can be added to a pet."""
        pet = Pet("Buddy", "Dog", 3, "None")
        task = Task("Walk", 30, "high", "exercise", "daily")
        pet.add_task(task)
        self.assertIn(task, pet.get_tasks())
        self.assertEqual(len(pet.get_tasks()), 1)

    def test_schedule_get_all_pet_tasks(self):
        """Test that Schedule can retrieve all tasks from owner's pets."""
        owner = PetOwner("Alice", 480, "None")
        pet1 = Pet("Buddy", "Dog", 3, "None")
        pet2 = Pet("Whiskers", "Cat", 2, "None")
        task1 = Task("Walk", 30, "high", "exercise", "daily")
        task2 = Task("Feed", 15, "medium", "feeding", "daily")
        pet1.add_task(task1)
        pet2.add_task(task2)
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        schedule = Schedule(owner)
        all_tasks = schedule.get_all_pet_tasks()
        self.assertEqual(len(all_tasks), 2)
        self.assertIn(task1, all_tasks)
    def test_task_completion(self):
        """Verify that calling mark_complete() changes the task's status."""
        task = Task("Walk", 30, "high", "exercise", "daily")
        self.assertEqual(task.status, "pending")
        task.mark_complete()
        self.assertEqual(task.status, "completed")

    def test_task_addition_to_pet(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet("Buddy", "Dog", 3, "None")
        initial_count = len(pet.get_tasks())
        task = Task("Walk", 30, "high", "exercise", "daily")
        pet.add_task(task)
        self.assertEqual(len(pet.get_tasks()), initial_count + 1)
