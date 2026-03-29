# PawPal+ Project Reflection

## 1. System Design
- A user should enter basic owner + pet info
- A user should be able add/edit tasks (duration + priority at minimum)
- Daily schedule/plan based on constraints and priorities


**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Answer:
1. PetOwner

Attributes:

name
available_time_per_day (in minutes or hours)
preferences (e.g., preferred walk times, task priorities)

Methods:

add_task(task)
remove_task(task)
get_tasks()

2. Pet

Attributes:

name
type (dog, cat, etc.)
age
special_needs (e.g., medication, diet)

Methods:

get_pet_info()

3. Task

(This is the most important object)

Attributes:

name (e.g., “Morning Walk”)
duration (in minutes)
priority (e.g., high, medium, low OR numeric)
category (feeding, walking, grooming, etc.)
frequency (daily, weekly)

Methods:

update_priority(new_priority)
update_duration(new_duration)
get_task_details()

4. Schedule

(Represents the daily plan)

Attributes:

tasks (list of Task objects)
total_time_used
remaining_time

Methods:

add_task(task)
remove_task(task)
calculate_total_time()
display_schedule()


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Answer:
- Added `self.pets = []` in `PetOwner.__init__()` to store a list of `Pet` objects.
- Added methods: `add_pet(pet: Pet)`, `remove_pet(pet: Pet)`, and `get_pets()` to manage pets.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Answer
 - Real time windows
 - total time availability
 - task importance
 - recurring cycle semantics
  - conflict/no-overlap warnings
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Answer:
 - speed over perfect optimization
 - The tradeoff is reasonable because it keeps the product usable now, while still being easy to extend later.
## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Answer:
I used Ai to specify design logics and debugging
-specifying files using the '#' symbol was really helpful

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

Answer:
 - There was a time when i made a mistake with a prompt. The AI generated a false suggestion in which I could not accept

 - I verfiying by comparing what I originally had and the suggested code given to see where the problem was
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Answer:
- Sorting by time, Conflict detection
 - It ensures schedule is chronologial, so owners day actually flows
  - To prevent impossible schedules (two tasks at same time)

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---
Answer:
-Due to all the tests cases passed, I am 100% confident
 - a test case would be 'No task at all' case

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Answer:
I am most satisfied with the UML diagram which guided me 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Answer: 
I would improve the schedule optimezer by upgrading to a constrained selection algorithm (knapsack-like with priority-weighted scoring) to maximize coverage within

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Answer:
Ai is a great assistant when it is given the right prompt. 
