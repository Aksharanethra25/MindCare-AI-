
import streamlit as st

st.set_page_config(
    page_title="MindCare AI",
    page_icon="💚",
    layout="wide"
)

st.title("💚 MindCare AI")

st.subheader(
    "Mental Wellness Screening & Support"
)

st.write(
    "Welcome to MindCare AI!"
)

st.markdown("---")

st.header("Your Mental Wellness Matters")

st.write(
    "Explore your emotional well-being "
    "through a simple and supportive assessment."
)

st.info(
    "This application is an educational "
    "wellness-support prototype, not a medical "
    "diagnosis or emergency service."
)

st.markdown("### What would you like to explore?")

if st.button("Start Wellness Assessment"):
    st.success("Wellness assessment module is coming soon!")

if st.button("Explore Support"):
    st.write(
        "You deserve support. Consider speaking "
        "with someone you trust or a qualified professional."
    )

st.markdown("---")

st.caption("MindCare AI | Neural Storm 2026")
