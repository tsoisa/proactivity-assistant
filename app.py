import streamlit as st
from tasks import TASKS
st.set_page_config(layout="wide")

s = st.session_state  # remembers things between clicks
s.setdefault("i", 0)
s.setdefault("history", [])

def respond(action):
    title, _, _, _, fix, correct = TASKS[s.i]
    if action == "use":
        action = "accepted_unedited" if s[f"code{s.i}"] == fix else "edited"
    s.history.append((s.i + 1, action, correct))
    s.i += 1

st.title("Proactivity Assistant")
st.caption("Suggestions are simulated (pre-written), not generated live.")

if s.i == len(TASKS):
    st.success("All tasks complete.")
    st.table(s.history)
    st.stop()

title, bug, line, why, fix, correct = TASKS[s.i]
st.subheader(f"Task {s.i + 1}/{len(TASKS)}: {title}")
left, right = st.columns(2)
left.code(bug, language="python", line_numbers=True, wrap_lines=True)
right.info(why)
right.text_area("Suggested fix (edit if needed)", fix, key=f"code{s.i}")
right.button("Use this code", on_click=respond, args=("use",))
right.button("Reject", on_click=respond, args=("rejected",))