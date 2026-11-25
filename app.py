import streamlit as st
from datetime import datetime
from tasks import TASKS

st.set_page_config(layout="wide")

DOWN_AFTER = 3 # unedited accepts before switching to Notify
UP_AFTER = 2 # tested 3 but too slow to return to Suggest so kept 2

s = st.session_state 
s.setdefault("i", 0)
s.setdefault("mode", "Suggest")
s.setdefault("unedited", 0)
s.setdefault("engaged", 0)
s.setdefault("revealed", False)
s.setdefault("reason", "Suggest mode: I'll show you the correction for each task, but you can edit it if you like.")
s.setdefault("log", [])

def log(action, note=""):
    correct = TASKS[s.i][5] if s.i < len(TASKS) and action != "mode change" else None
    s.log.append({"time": datetime.now().strftime("%H:%M:%S"), "task": s.i + 1,
                  "mode": s.mode, "action": action, "fix correct": correct, "note": note})

def set_mode(mode, reason):
    # Reset counters on every change of mode so one action can't reset the other 
    s.mode, s.reason = mode, reason
    s.unedited = s.engaged = 0
    log("mode change", f"to {mode}")

def respond(action):
    # Sensing: group the response as accepted unedited, edited or rejected
    fix, correct = TASKS[s.i][4], TASKS[s.i][5]
    if action == "use":
        action = "accepted_unedited" if s[f"code{s.i}"] == fix else "edited"
    log(action, "over-reliance: wrong fix accepted unedited" if action == "accepted_unedited" and not correct else "")

    if action == "accepted_unedited":
        s.unedited, s.engaged = s.unedited + 1, 0
    else:
        s.engaged, s.unedited = s.engaged + 1, 0

    if s.mode == "Suggest" and s.unedited >= DOWN_AFTER:
        set_mode("Notify", f"Notify: the last {DOWN_AFTER} suggestions were used without you making a change. "
                           "Check the code yourself first, then ask for my fix if you want it.")
    elif s.mode == "Notify" and s.engaged >= UP_AFTER:
        set_mode("Suggest", f"Suggest is back on: you edited or rejected the last {UP_AFTER} suggestions.")
    s.i += 1
    s.revealed = False

def reveal():
    s.revealed = True
    log("asked for suggestion")

def override():
    new = "Notify" if s.mode == "Suggest" else "Suggest"
    set_mode(new, f"You turned on {new} mode.")

# Page
st.title("Proactivity Assistant")
st.caption("Suggestions are simulated (pre-written), not generated live.")

# Feedback: show the current mode and why it changed
top = st.columns([3, 1])
(top[0].info if s.mode == "Suggest" else top[0].warning)(f"**Mode: {s.mode}**  \n{s.reason}")
top[1].button(f"Switch to {'Notify' if s.mode == 'Suggest' else 'Suggest'}", on_click=override)

if s.i == len(TASKS):
    st.success("All tasks completed! Thanks for participating.")
    misses = sum("over-reliance" in r["note"] for r in s.log)
    st.write(f"Incorrect fixes you used without changing them: **{misses} of 3**")
else:
    title, bug, line, why, fix, correct = TASKS[s.i]
    st.subheader(f"Task {s.i + 1}/{len(TASKS)}: {title}")
    left, right = st.columns(2)
    left.code(bug, language="python", line_numbers=True, wrap_lines=True)

    if s.mode == "Notify" and not s.revealed:
        right.warning(f"Look at **line {line}**. Something there might be wrong.")
        right.button("Show me the fix", on_click=reveal)
    else:
        right.info(why)
        right.text_area("My suggested fix (you can change it)", fix, key=f"code{s.i}")
        right.button("Use this code", on_click=respond, args=("use",))
        right.button("Reject", on_click=respond, args=("rejected",))

with st.expander("Interaction log"):
    st.table(s.log)
