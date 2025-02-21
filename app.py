import streamlit as st
import json
import uuid
import os

# Function to ensure all tasks have IDs
def validate_task(task):
    if 'id' not in task:
        task['id'] = str(uuid.uuid4())
    if 'completed' not in task:
        task['completed'] = False
    return task

# Function to save tasks to file
def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(st.session_state.tasks, f)

# Function to load tasks safely
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            return [validate_task(task) for task in tasks]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Initialize session state with validation
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# Rest of the app code remains the same until the task display section
# ... [Keep all previous code until task display section] ...

# Modified task display section with safer key handling
if not st.session_state.tasks:
    st.info("🌟 No tasks found! Add a new task above to get started!")
else:
    st.subheader("📝 Your Tasks:")
    for index, task in enumerate(st.session_state.tasks):
        task = validate_task(task)  # Ensure task has required fields
        cols = st.columns([1, 4, 2, 2])
        with cols[0]:
            st.checkbox(
                "Completed", 
                value=task['completed'],
                key=f"check_{task['id']}",
                on_change=lambda t=task: t.update({'completed': not t['completed']})
            )
        # Rest of the task display code remains the same
        # ... [Keep the rest of the display code] ...

# Modified file upload handler
def load_tasks_from_file(uploaded_file):
    try:
        tasks = json.load(uploaded_file)
        st.session_state.tasks = [validate_task(task) for task in tasks]
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

# Keep the rest of the code the same
# ... [Remainder of the original code] ...
