import streamlit as st
import json
import time

# Load tasks from JSON file
TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"To Do": {}, "In Progress": {}, "Done": {}}

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

if 'current_task' not in st.session_state:
    st.session_state.current_task = None

st.title("Kanban Board")

# If a task is selected, open the task page
if st.session_state.current_task:
    st.header(f"Task: {st.session_state.current_task}")
    task_data = st.session_state.tasks.get("To Do", {}).get(st.session_state.current_task, {})
    
    speed = st.number_input("Speed (RPM)", value=task_data.get("speed", 0))
    feed_rate = st.number_input("Feed Rate (mm/min)", value=task_data.get("feed_rate", 0))
    duration = st.number_input("Duration (s)", value=task_data.get("duration", 0))
    
    if st.button("Submit Data"):
        # Save machining data
        st.session_state.tasks["To Do"].pop(st.session_state.current_task, None)
        st.session_state.tasks["In Progress"][st.session_state.current_task] = {
            "speed": speed,
            "feed_rate": feed_rate,
            "duration": duration
        }
        save_tasks(st.session_state.tasks)

        
        # Simulate processing time and move to Done
        time.sleep(5)
        st.session_state.tasks["In Progress"].pop(st.session_state.current_task, None)
        st.session_state.tasks["Done"][st.session_state.current_task] = {
            "speed": speed,
            "feed_rate": feed_rate,
            "duration": duration
        }
        save_tasks(st.session_state.tasks)
        
        # Reset task and return to main page
        st.session_state.current_task = None

else:
    # Display Kanban Board
    cols = st.columns(3)
    statuses = ['To Do', 'In Progress', 'Done']

    for i, status in enumerate(statuses):
        with cols[i]:
            st.header(status)
            for task, data in st.session_state.tasks[status].items():
                if status == "Done":
                    with st.expander(task):
                        st.write(f"**Speed:** {data['speed']} RPM")
                        st.write(f"**Feed Rate:** {data['feed_rate']} mm/min")
                        st.write(f"**Duration:** {data['duration']} s")
                else:
                    if st.button(task, key=f"task_{task}"):
                        st.session_state.current_task = task

    

