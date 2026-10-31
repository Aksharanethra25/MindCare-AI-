
import streamlit as st

st.set_page_config(
    page_title="MindCare AI",
    page_icon="💚",
    layout="centered"
)

st.title("💚 MindCare AI")
st.subheader("Mental Wellness Check-in & Support")

st.write(
    "A simple space to reflect on your emotional "
    "wellbeing and explore supportive resources."
)

st.info(
    "This is an educational wellbeing prototype. "
    "It does not diagnose mental health conditions "
    "or provide emergency services."
)

st.header("Daily Wellbeing Check-in")

mood = st.radio(
    "1. How has your mood been today?",
    ["Very good", "Good", "Okay", "Not very good"]
)

energy = st.radio(
    "2. How has your energy level been today?",
    ["High", "Normal", "Low", "Very low"]
)

sleep = st.radio(
    "3. How would you describe your sleep?",
    ["Good", "Fair", "Poor", "Not sure"]
)

support = st.radio(
    "4. Would you like to explore support options?",
    ["Yes", "Maybe later", "No"]
)

journal = st.text_area(
    "Would you like to write anything about your day? (Optional)",
    placeholder="Write only what you feel comfortable sharing..."
)

if st.button("Submit Check-in"):
    st.success("Thank you for completing your check-in.")

    st.write("Your responses:")
    st.write("**Mood:**", mood)
    st.write("**Energy:**", energy)
    st.write("**Sleep:**", sleep)

    if support == "Yes":
        st.info(
            "Consider speaking with a trusted adult, "
            "school counsellor, or qualified mental "
            "health professional."
        )
    else:
        st.write("You can explore support whenever you feel ready.")

    st.caption(
        "Your journal entry is not saved by this prototype."
    )

st.divider()

st.header("Support and Safety")

st.write(
    "You deserve care and support. Consider talking "
    "to someone you trust if you are having a difficult time."
)

st.write(
    "If you are in immediate danger, contact a trusted "
    "adult and your local emergency service."
)

st.caption("MindCare AI | Neural Storm 2026")
