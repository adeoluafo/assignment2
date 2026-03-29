import streamlit as st
from pawpal_system import PetOwner, Pet, Task, Schedule
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize PetOwner in session_state
if "owner" not in st.session_state:
    st.session_state.owner = PetOwner("Default Owner", 480, "No preferences set")

owner = st.session_state.owner

st.subheader("Owner Information")
col1, col2 = st.columns(2)
with col1:
    new_owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
    if new_owner_name != owner.name:
        owner.name = new_owner_name
with col2:
    new_available_time = st.number_input(
        "Available time (minutes/day)", 
        min_value=1, 
        max_value=1440, 
        value=owner.available_time_per_day,
        key="available_time_input"
    )
    if new_available_time != owner.available_time_per_day:
        owner.available_time_per_day = new_available_time

st.markdown("### Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="species_select")
with col3:
    special_needs = st.text_input("Special needs", value="None", key="special_needs_input")

if st.button("Add Pet"):
    if pet_name:
        new_pet = Pet(pet_name, species, 1, special_needs)
        owner.add_pet(new_pet)
        st.success(f"Added {pet_name} the {species}!")
    else:
        st.error("Pet name cannot be empty.")

if owner.get_pets():
    st.write(f"**Owner's Pets ({len(owner.get_pets())}):**")
    for idx, pet in enumerate(owner.get_pets()):
        st.write(f"{idx + 1}. {pet.get_pet_info()}")
else:
    st.info("No pets added yet. Add one above.")

st.markdown("### Add Tasks to Pets")
if owner.get_pets():
    selected_pet = st.selectbox(
        "Select a pet",
        [pet.name for pet in owner.get_pets()],
        key="pet_select"
    )
    
    task_name = st.text_input("Task name", value="Morning walk", key="task_name_input")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30, key="duration_input")
    priority = st.selectbox("Priority", ["low", "medium", "high"], key="priority_select")
    category = st.selectbox("Category", ["feeding", "exercise", "grooming", "play", "medication"], key="category_select")
    
    if st.button("Add Task"):
        if task_name:
            new_task = Task(task_name, duration, priority, category, "daily")
            pet = next(p for p in owner.get_pets() if p.name == selected_pet)
            pet.add_task(new_task)
            st.success(f"Added '{task_name}' to {selected_pet}!")
        else:
            st.error("Task name cannot be empty.")
    
    st.markdown("#### Tasks by Pet")
    for pet in owner.get_pets():
        pet_tasks = pet.get_tasks()
        if pet_tasks:
            st.write(f"**{pet.name}:**")
            for task in pet_tasks:
                st.write(f"  - {task.get_task_details()}")
        else:
            st.write(f"**{pet.name}:** No tasks yet.")
else:
    st.info("Add a pet first to assign tasks.")



st.divider()

st.subheader("Generate Schedule")
st.caption("Build a daily schedule based on owner's available time and pet tasks.")

if st.button("Generate schedule"):
    owner = st.session_state.owner
    all_pet_tasks = []
    
    # Collect all tasks from all pets
    for pet in owner.get_pets():
        all_pet_tasks.extend(pet.get_tasks())
    
    if all_pet_tasks:
        # Create a schedule and add tasks
        schedule = Schedule(owner)
        
        # Sort tasks by priority (high first) and duration
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(all_pet_tasks, key=lambda t: (priority_order.get(t.priority, 3), t.duration))
        
        # Add tasks to schedule until we run out of time or tasks
        for task in sorted_tasks:
            if schedule.remaining_time >= task.duration:
                schedule.add_task(task)
        
        # Display the schedule
        st.success("Schedule generated!")
        st.subheader("Your Daily Schedule")
        schedule.display_schedule()
        
        # Show details
        st.markdown("#### Schedule Details")
        st.write(f"**Owner:** {owner.name}")
        st.write(f"**Available Time:** {owner.available_time_per_day} minutes")
        st.write(f"**Scheduled Tasks:** {len(schedule.tasks)}")
        st.write(f"**Total Time Used:** {schedule.total_time_used} minutes")
        st.write(f"**Remaining Time:** {schedule.remaining_time} minutes")
        
        if schedule.remaining_time > 0:
            st.info(f"You have {schedule.remaining_time} minutes left in your day!")
        else:
            st.warning("Your schedule is fully booked!")
    else:
        st.warning("No tasks found. Add tasks to pets first.")
