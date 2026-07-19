import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="VTI Okara Timetable Generator",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Vocational Training Institute Okara")
st.subheader("Automatic Weekly Timetable Generator")

# -----------------------------
# Institute Information
# -----------------------------
institute = st.text_input(
    "Institute Name",
    value="Vocational Training Institute Okara"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Settings")

days = st.sidebar.multiselect(
    "Working Days",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
)

periods = st.sidebar.slider(
    "Lectures Per Day",
    4,
    10,
    6
)

lecture_duration = st.sidebar.selectbox(
    "Lecture Duration",
    [30, 45, 60],
    index=2
)

# -----------------------------
# Trades
# -----------------------------
st.header("Trades / Classes")

default_trades = """Computer Applications
General Electrician
Solar Technician
Motorcycle Mechanic
Refrigeration & Air Conditioning
Dress Making"""

trade_text = st.text_area(
    "Enter one trade per line",
    default_trades,
    height=170
)

trades = [i.strip() for i in trade_text.split("\n") if i.strip()]

# -----------------------------
# Instructors
# -----------------------------
st.header("Instructors")

default_instructors = """Mr. Ali
Mr. Ahmad
Mr. Bilal
Mr. Hamza
Mr. Rashid
Mr. Faisal"""

teacher_text = st.text_area(
    "Enter one instructor per line",
    default_instructors,
    height=170
)

teachers = [i.strip() for i in teacher_text.split("\n") if i.strip()]

# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate Timetable"):

    if len(days) == 0:
        st.error("Please select working days.")
        st.stop()

    if len(trades) == 0:
        st.error("Please enter at least one trade.")
        st.stop()

    if len(teachers) == 0:
        st.error("Please enter at least one instructor.")
        st.stop()

    timetable = pd.DataFrame(index=days)

    for p in range(1, periods + 1):
        timetable[f"Period {p}"] = ""

    for day in days:
        used_teachers = []

        for p in range(periods):

            trade = random.choice(trades)

            available = [t for t in teachers if t not in used_teachers]

            if len(available) == 0:
                used_teachers = []
                available = teachers

            teacher = random.choice(available)
            used_teachers.append(teacher)

            timetable.iloc[days.index(day), p] = f"{trade}\n({teacher})"

    st.success("Timetable Generated Successfully!")

    st.header(institute)

    st.write(f"Lecture Duration: {lecture_duration} Minutes")

    st.dataframe(timetable, use_container_width=True)

    csv = timetable.to_csv().encode("utf-8")

    st.download_button(
        "⬇ Download Timetable (CSV)",
        csv,
        "VTI_Okara_Timetable.csv",
        "text/csv"
    )
