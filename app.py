import streamlit as st
import json
import uuid
import os

# Function to save tasks to file
def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(st.session_state.tasks, f)

# Function to load tasks from uploaded file
def load_tasks_from_file(uploaded_file):
    try:
        tasks = json.load(uploaded_file)
        st.session_state.tasks = tasks
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

# Initialize session state
if 'tasks' not in st.session_state:
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []

# App header
st.title("🚀 Streamlit To-Do List Manager")
st.markdown("---")

# Add new task form
with st.form("new_task"):
    task_input = st.text_input("Add a new task:", placeholder="Enter your task here...")
    add_cols = st.columns([3, 1])
    with add_cols[0]:
        submitted = st.form_submit_button("➕ Add Task")
    with add_cols[1]:
        clear_all = st.form_submit_button("❌ Clear All")
    
    if submitted and task_input:
        new_task = {
            "id": str(uuid.uuid4()),
            "description": task_input.strip(),
            "completed": False
        }
        st.session_state.tasks.append(new_task)
        st.rerun()
    
    if clear_all:
        st.session_state.tasks = []
        st.rerun()

# Display tasks
if not st.session_state.tasks:
    st.info("🌟 No tasks found! Add a new task above to get started!")
else:
    st.subheader("📝 Your Tasks:")
    for task in st.session_state.tasks:
        cols = st.columns([1, 4, 2, 2])
        with cols[0]:
            st.checkbox(
                "Completed", 
                value=task['completed'],
                key=f"check_{task['id']}",
                on_change=lambda t=task: t.update({'completed': not t['completed']})
            )
        with cols[1]:
            if task['completed']:
                st.markdown(f"<s>{task['description']}</s>", unsafe_allow_html=True)
            else:
                st.markdown(task['description'])
        with cols[2]:
            if st.button("🔄 Toggle", key=f"toggle_{task['id']}"):
                task['completed'] = not task['completed']
                st.rerun()
        with cols[3]:
            if st.button("🗑️ Delete", key=f"delete_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                st.rerun()
    st.markdown("---")

# File management in sidebar
with st.sidebar:
    st.header("⚙️ Manage Tasks")
    if st.button("💾 Save Tasks to File"):
        save_tasks()
        st.success("Tasks saved successfully!")
    
    st.markdown("---")
    st.subheader("Load Tasks")
    uploaded_file = st.file_uploader("Upload tasks file", type=['json'])
    if uploaded_file is not None:
        load_tasks_from_file(uploaded_file)
        st.rerun()

# Display statistics
completed_tasks = sum(1 for task in st.session_state.tasks if task['completed'])
st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Statistics:**\n"
                    f"- Total tasks: {len(st.session_state.tasks)}\n"
                    f"- Completed: {completed_tasks}\n"
                    f"- Remaining: {len(st.session_state.tasks) - completed_tasks}")
