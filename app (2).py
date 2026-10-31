
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="MindCare AI",
    page_icon="💚",
    layout="wide"
)

# SESSION DATA
if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR
st.sidebar.title("💚 MindCare AI")
st.sidebar.caption("Your Wellbeing Companion")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Wellbeing Assessment",
        "AI Support Assistant",
        "Wellbeing Insights",
        "AI / ML Demonstration",
        "Support Resources"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Educational prototype | Not a medical diagnosis")

# DASHBOARD
if page == "Dashboard":

    st.title("💚 MindCare AI")
    st.subheader("Mental Wellness & Support Platform")

    st.info(
        "A privacy-conscious educational platform "
        "to explore emotional wellbeing and supportive resources."
    )

    st.header("Welcome to your wellbeing dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Assessments completed", len(st.session_state.history))

    with col2:
        st.metric("Support conversations", len(st.session_state.messages))

    with col3:
        st.metric("Platform", "Active")

    st.divider()

    st.subheader("Explore MindCare AI")

    st.write("📝 Complete a wellbeing assessment.")
    st.write("💬 Explore the support assistant.")
    st.write("📊 View your wellbeing history.")
    st.write("🤖 Explore the AI/ML demonstration.")
    st.write("❤️ Find helpful support resources.")

    st.caption("Your wellbeing matters. Take things one step at a time.")

# WELLBEING ASSESSMENT
elif page == "Wellbeing Assessment":

    st.title("📝 Wellbeing Assessment")

    st.write(
        "Reflect on your recent experiences. "
        "There are no right or wrong answers."
    )

    with st.form("assessment_form"):

        mood = st.select_slider(
            "How would you describe your mood?",
            options=["Very low", "Low", "Okay", "Good", "Very good"]
        )

        stress = st.select_slider(
            "How manageable has your daily stress felt?",
            options=["Very difficult", "Difficult", "Moderate",
                     "Manageable", "Very manageable"]
        )

        sleep = st.select_slider(
            "How has your sleep been?",
            options=["Very poor", "Poor", "Fair", "Good", "Very good"]
        )

        energy = st.select_slider(
            "How has your energy been?",
            options=["Very low", "Low", "Average", "Good", "High"]
        )

        focus = st.select_slider(
            "How has your concentration been?",
            options=["Very difficult", "Difficult", "Average",
                     "Good", "Very good"]
        )

        activity = st.selectbox(
            "How often do you take part in activities you enjoy?",
            ["Daily", "Several times a week", "Sometimes", "Rarely"]
        )

        submitted = st.form_submit_button("Submit Assessment")

    if submitted:

        record = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Mood": mood,
            "Stress": stress,
            "Sleep": sleep,
            "Energy": energy,
            "Focus": focus,
            "Activity": activity
        }

        st.session_state.history.append(record)

        st.success("Your assessment has been completed!")

        st.subheader("Your responses")

        st.write("**Mood:**", mood)
        st.write("**Stress:**", stress)
        st.write("**Sleep:**", sleep)
        st.write("**Energy:**", energy)
        st.write("**Focus:**", focus)

        st.info(
            "These responses are reflections, not a diagnosis "
            "or a measure of clinical risk."
        )

        st.write("### A supportive suggestion")

        if mood in ["Very low", "Low"]:
            st.write(
                "Consider talking with someone you trust "
                "about how you have been feeling."
            )

        elif stress in ["Very difficult", "Difficult"]:
            st.write(
                "Try taking a short break and identifying "
                "one manageable task at a time."
            )

        elif sleep in ["Very poor", "Poor"]:
            st.write(
                "A consistent bedtime routine may help. "
                "Consider discussing ongoing sleep difficulties "
                "with a healthcare professional."
            )

        else:
            st.write(
                "Consider continuing activities and routines "
                "that help you feel supported."
            )

# SUPPORT ASSISTANT
elif page == "AI Support Assistant":

    st.title("💬 MindCare Support Assistant")

    st.write(
        "Ask general questions about wellbeing, "
        "healthy routines and finding support."
    )

    st.info(
        "This is a simple rule-based demonstration, "
        "not a clinical AI chatbot or emergency service."
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your question here...")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        question = user_input.lower()

        if any(word in question for word in
               ["stress", "pressure", "overwhelmed"]):

            answer = (
                "It can help to pause, take a comfortable break "
                "and speak with someone you trust. "
                "You do not have to manage everything alone."
            )

        elif any(word in question for word in
                 ["sleep", "tired", "rest"]):

            answer = (
                "A regular sleep routine, a calm environment "
                "and reducing screen use before bedtime "
                "may support better rest."
            )

        elif any(word in question for word in
                 ["study", "focus", "concentration"]):

            answer = (
                "Try dividing your work into smaller tasks "
                "and taking short breaks between study sessions."
            )

        elif any(word in question for word in
                 ["sad", "lonely", "upset"]):

            answer = (
                "Your feelings deserve attention. "
                "Consider speaking with a trusted adult, "
                "school counsellor or qualified professional."
            )

        elif any(word in question for word in
                 ["help", "support", "counsellor"]):

            answer = (
                "You can reach out to a trusted adult, "
                "school counsellor or qualified mental "
                "health professional."
            )

        else:

            answer = (
                "Thank you for sharing. I can offer general "
                "wellbeing information, but I cannot diagnose "
                "or assess a crisis. Consider speaking with "
                "someone you trust for personal support."
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# WELLBEING INSIGHTS
elif page == "Wellbeing Insights":

    st.title("📊 Wellbeing Insights")

    if len(st.session_state.history) == 0:

        st.info(
            "Complete an assessment first to see your "
            "personal session history."
        )

    else:

        df = pd.DataFrame(st.session_state.history)

        st.subheader("Assessment History")

        st.dataframe(df, use_container_width=True)

        st.subheader("Your recorded responses")

        st.write("Mood responses")
        st.bar_chart(df["Mood"].value_counts())

        st.write("Sleep responses")
        st.bar_chart(df["Sleep"].value_counts())

        st.write("Energy responses")
        st.bar_chart(df["Energy"].value_counts())

        st.caption(
            "These charts describe your recorded answers. "
            "They do not measure mental health conditions."
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download My Assessment History",
            data=csv,
            file_name="mindcare_history.csv",
            mime="text/csv"
        )

# AI / ML DEMONSTRATION
elif page == "AI / ML Demonstration":

    st.title("🤖 AI / ML Demonstration")

    st.write(
        "This educational demonstration uses synthetic "
        "data to show how machine learning can identify "
        "patterns in sample wellbeing information."
    )

    st.warning(
        "The sample data is artificial. The model does not "
        "evaluate real people, diagnose conditions or detect crises."
    )

    if st.button("Run Machine Learning Demonstration"):

        np.random.seed(42)

        sample_data = np.vstack([
            np.random.normal([4, 4, 4], 0.7, (30, 3)),
            np.random.normal([2, 2, 2], 0.7, (30, 3)),
            np.random.normal([3, 4, 2], 0.7, (30, 3))
        ])

        sample_data = np.clip(sample_data, 1, 5)

        model = KMeans(
            n_clusters=3,
            random_state=42,
            n_init=10
        )

        clusters = model.fit_predict(sample_data)

        results = pd.DataFrame({
            "Sample Mood": sample_data[:, 0],
            "Sample Sleep": sample_data[:, 1],
            "Sample Energy": sample_data[:, 2],
            "Pattern Group": clusters
        })

        st.success("Machine learning demonstration completed!")

        st.metric("Synthetic samples analysed", len(results))

        st.write("Sample results")
        st.dataframe(results.head(10), use_container_width=True)

        st.write("Pattern group distribution")
        st.bar_chart(
            results["Pattern Group"].value_counts().sort_index()
        )

        st.write("Cluster centres")
        st.dataframe(
            pd.DataFrame(
                model.cluster_centers_,
                columns=["Mood", "Sleep", "Energy"]
            )
        )

        st.caption(
            "K-Means is an unsupervised machine-learning algorithm. "
            "These groups have no clinical meaning."
        )

# SUPPORT RESOURCES
elif page == "Support Resources":

    st.title("❤️ Support Resources")

    st.subheader("You deserve support.")

    st.write(
        "Consider speaking with someone you trust "
        "if you are experiencing difficulties."
    )

    st.markdown("""
    ### Available support options

    - Trusted family member or adult
    - School or college counsellor
    - Qualified mental health professional
    - Local healthcare services

    ### Emergency support

    If you or someone else is in immediate danger,
    contact a trusted adult and local emergency services.

    In India, emergency assistance is available through 112.
    """)

    st.info(
        "MindCare AI is an educational prototype, "
        "not a substitute for professional care."
    )

# FOOTER
st.divider()

st.caption(
    "💚 MindCare AI | Neural Storm 2026 | "
    "Educational Wellbeing Support Prototype"
)
