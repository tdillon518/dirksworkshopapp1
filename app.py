import streamlit as st
import os
import json

# Name of the file where tasks will be saved/loaded
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        try:
            tasks = json.load(file)
        except json.JSONDecodeError:
            tasks = []
    return tasks

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def main():
    st.title("My To-Do List")

    # Initialize tasks in session state
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

    # Text input for a new task
    new_task = st.text_input("Add a new task", "")
    if st.button("Add Task"):
        if new_task.strip():
            st.session_state.tasks.append({"task": new_task, "completed": False})
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()

    st.subheader("Current Tasks")
    if len(st.session_state.tasks) == 0:
        st.write("No tasks yet. Add one above!")
    else:
        for i, task_item in enumerate(st.session_state.tasks):
            task_text = task_item["task"]
            completed = task_item["completed"]

            # Use columns for "Complete" / "Delete" buttons
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            with col1:
                if completed:
                    # Strike-through for completed tasks
                    st.markdown(f"~~{task_text}~~")
                else:
                    st.write(task_text)

            with col2:
                complete_button_text = "Unmark" if completed else "Complete"
                if st.button(complete_button_text, key=f"complete_{i}"):
                    st.session_state.tasks[i]["completed"] = not completed
                    save_tasks(st.session_state.tasks)
                    st.experimental_rerun()

            with col3:
                if st.button("Delete", key=f"delete_{i}"):
                    st.session_state.tasks.pop(i)
                    save_tasks(st.session_state.tasks)
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
