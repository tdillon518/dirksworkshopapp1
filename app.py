import streamlit as st
import json
import uuid
import os

# Function to ensure all tasks have required fields
def validate_task(task):
    if not isinstance(task, dict):
        task = {"description": str(task)}
    
    defaults = {
        'id': str(uuid.uuid4()),
        'completed': False,
        'description': ''
    }
    
    # Update task with any missing default values
    for key, value in defaults.items():
        if key not in task:
            task[key] = value
    
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

# App header
st.title("🚀 Streamlit To-Do List Manager")
st.markdown("---")

# Add new task section
st.subheader("➕ Add New Task")
new_task = st.text_input(
    "Task description:",
    value=st.session_state.get('new_task_input', ''),
    placeholder="Enter your task here...",
    key="task_input"
)

col1, col2, col3 = st.columns([2, 3, 2])
with col1:
    if st.button("✅ Add Task", use_container_width=True):
        if new_task.strip():
            st.session_state.tasks.append({
                "id": str(uuid.uuid4()),
                "description": new_task.strip(),
                "completed": False
            })
            st.session_state.new_task_input = ''  # Clear input
            save_tasks()
            st.rerun()

with col2:
    if st.button("🗑️ Clear All Tasks", use_container_width=True):
        st.session_state.tasks = []
        st.session_state.new_task_input = ''
        save_tasks()
        st.rerun()

with col3:
    if st.button("💾 Save to File", use_container_width=True):
        save_tasks()
        st.success("Tasks saved successfully!")

# Display tasks
if not st.session_state.tasks:
    st.info("🌟 No tasks found! Add a new task above to get started!")
else:
    st.subheader("📝 Your Tasks:")
    for index, task in enumerate(st.session_state.tasks):
        task = validate_task(task)  # Ensure task has required fields
        cols = st.columns([1, 4, 2, 2])
        
        with cols[0]:
            if st.checkbox(
                "Completed", 
                value=task['completed'],
                key=f"check_{task['id']}"
            ):
                task['completed'] = True
            else:
                task['completed'] = False

        with cols[1]:
            if task['completed']:
                st.markdown(f"<s>{task['description']}</s>", unsafe_allow_html=True)
            else:
                st.markdown(task['description'])

        with cols[2]:
            if st.button("🔄 Toggle", key=f"toggle_{task['id']}"):
                task['completed'] = not task['completed']
                save_tasks()
                st.rerun()

        with cols[3]:
            if st.button("🗑️ Delete", key=f"delete_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                save_tasks()
                st.rerun()

    st.markdown("---")

# File management in sidebar
with st.sidebar:
    st.header("⚙️ Manage Tasks")
    st.markdown("---")
    st.subheader("Load Tasks")
    uploaded_file = st.file_uploader("Upload tasks file", type=['json'])
    
    if uploaded_file is not None:
        try:
            tasks = json.load(uploaded_file)
            st.session_state.tasks = [validate_task(task) for task in tasks]
            save_tasks()
            st.rerun()
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

# Display statistics
completed_tasks = sum(1 for task in st.session_state.tasks if task['completed'])
st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Statistics:**\n"
                   f"- Total tasks: {len(st.session_state.tasks)}\n"
                   f"- Completed: {completed_tasks}\n"
                   f"- Remaining: {len(st.session_state.tasks) - completed_tasks}")
