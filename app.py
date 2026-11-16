import streamlit as st
from datetime import datetime
from tasks import TASKS

st.set_page_config(layout="wide")

DOWN_AFTER = 3  # unedited accepts in a row before stepping down to Notify
UP_AFTER = 2    # engaged responses (edit or reject) in a row before stepping back up

s = st.session_state  # remembers things between clicks
s.setdefault("i", 0)
s.setdefault("mode", "Suggest")
s.setdefault("unedited", 0)
s.setdefault("engaged", 0)
s.setdefault("revealed", False)
s.setdefault("reason", "Starting in Suggest mode: full fixes are shown.")
s.setdefault("log", [])

def log(action, note=""):
    correct = TASKS[s.i][5] if s.i < len(TASKS) and action != "mode change" else None
    s.log.append({"time": datetime.now().strftime("%H:%M:%S"), "task": s.i + 1,
                  "mode": s.mode, "action": action, "fix correct": correct, "note": note})

def set_mode(mode, reason):
    s.mode, s.reason = mode, reason
    s.unedited = s.engaged = 0
    log("mode change", f"to {mode}")

def respond(action):
    fix, correct = TASKS[s.i][4], TASKS[s.i][5]
    if action == "use":
        action = "accepted_unedited" if s[f"code{s.i}"] == fix else "edited"
    log(action, "over-reliance: wrong fix accepted unedited" if action == "accepted_unedited" and not correct else "")

    if action == "accepted_unedited":
        s.unedited, s.engaged = s.unedited + 1, 0
    else:
        s.engaged, s.unedited = s.engaged + 1, 0

    if s.mode == "Suggest" and s.unedited >= DOWN_AFTER:
        set_mode("Notify", f"Switched to Notify: the last {DOWN_AFTER} suggestions were used without changes. "
                           "Check the code yourself first, then ask for my fix if you want it.")
    elif s.mode == "Notify" and s.engaged >= UP_AFTER:
        set_mode("Suggest", f"Back to Suggest: you edited or rejected the last {UP_AFTER} suggestions.")
    s.i += 1
    s.revealed = False

def reveal():
    s.revealed = True
    log("asked for suggestion")

def override():
    new = "Notify" if s.mode == "Suggest" else "Suggest"
    set_mode(new, f"You switched to {new} mode yourself.")

# --- Page ------------------------------------------------------------------
st.title("Proactivity Assistant")
st.caption("Suggestions are simulated (pre-written), not generated live.")

top = st.columns([3, 1])
(top[0].info if s.mode == "Suggest" else top[0].warning)(f"**Mode: {s.mode}**  \n{s.reason}")
top[1].button(f"Switch to {'Notify' if s.mode == 'Suggest' else 'Suggest'}", on_click=override)

if s.i == len(TASKS):
    st.success("All tasks complete.")
    misses = sum("over-reliance" in r["note"] for r in s.log)
    st.write(f"Wrong fixes accepted without changes: **{misses} of 3**")
else:
    title, bug, line, why, fix, correct = TASKS[s.i]
    st.subheader(f"Task {s.i + 1}/{len(TASKS)}: {title}")
    left, right = st.columns(2)
    left.code(bug, language="python", line_numbers=True, wrap_lines=True)

    if s.mode == "Notify" and not s.revealed:
        right.warning(f"I spotted a possible issue on **line {line}**.")
        right.button("Show my suggestion", on_click=reveal)
    else:
        right.info(why)
        right.text_area("Suggested fix (edit if needed)", fix, key=f"code{s.i}")
        right.button("Use this code", on_click=respond, args=("use",))
        right.button("Reject", on_click=respond, args=("rejected",))

with st.expander("Interaction log"):
    st.table(s.log)
