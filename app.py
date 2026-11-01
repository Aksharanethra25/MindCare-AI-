import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from sklearn.cluster import KMeans
from PIL import Image
import io
import random

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except Exception:
    MEDIAPIPE_AVAILABLE = False

st.set_page_config(
    page_title="MindCare AI",
    page_icon="💚",
    layout="wide"
)

# ================= SESSION DATA =================

for key, default in {
    "history": [],
    "messages": [],
    "mood_log": [],
    "activities": [],
    "game_points": 0,
    "game_history": [],
    "memory_sequence": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ================= BEAUTIFUL DESIGN =================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Manrope:wght@600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
    radial-gradient(circle at 8% 5%, #dff8ed, transparent 30%),
    radial-gradient(circle at 95% 10%, #eee5ff, transparent 28%),
    linear-gradient(135deg, #f7fffc, #f7f7ff, #fff9f3);
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #153b35;
}

.hero {
    padding: 35px;
    border-radius: 25px;
    color: white;
    background: linear-gradient(115deg, #073b35, #087f70, #35b995);
    box-shadow: 0 12px 30px #087f7025;
}

.hero h1 {
    color: white;
    font-size: 2.5rem;
}

.hero p {
    color: #e7fff7;
    font-size: 1.1rem;
}

.panel {
    background: white;
    border: 1px solid #e4f0eb;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 12px;
    box-shadow: 0 5px 20px #194a3d0d;
}

.feature {
    background: linear-gradient(145deg, white, #effbf7);
    border: 1px solid #dcefe8;
    border-radius: 18px;
    padding: 18px;
    min-height: 145px;
}

div.stButton > button {
    border-radius: 12px;
    border: 0;
    font-weight: bold;
    background: linear-gradient(100deg, #087f70, #31b78f);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #effbf6, #f4f1ff);
}
</style>
""", unsafe_allow_html=True)


# ================= LANGUAGES =================

LANGUAGES = ["English", "தமிழ்", "हिन्दी", "తెలుగు"]

TEXT = {
    "English": {
        "welcome": "Welcome to MindCare AI — your friendly space for reflection, encouragement and everyday wellbeing.",
        "stress": "Take a comfortable pause, breathe naturally and focus on one manageable task.",
        "sleep": "A consistent sleep routine and a calm wind-down may support better rest.",
        "study": "Break your work into smaller tasks and take short breaks.",
        "sad": "Your feelings deserve care. Consider speaking with someone you trust.",
        "general": "Thank you for sharing. I can offer general wellbeing information, not a diagnosis.",
        "crisis": "Please contact a trusted adult or qualified professional now. If anyone is in immediate danger in India, call 112 or go to the nearest emergency department."
    },
    "தமிழ்": {
        "welcome": "MindCare AI-க்கு வரவேற்கிறோம். உங்கள் நலனுக்கான நட்பு தளம் இது.",
        "stress": "சிறிது ஓய்வு எடுத்து இயல்பாக சுவாசிக்கவும். ஒரு சிறிய பணியுடன் தொடங்குங்கள்.",
        "sleep": "தினமும் ஒரே நேரத்தில் தூங்கும் பழக்கம் ஓய்வுக்கு உதவலாம்.",
        "study": "படிப்பைச் சிறிய பகுதிகளாகப் பிரித்து இடையில் ஓய்வு எடுக்கவும்.",
        "sad": "உங்கள் உணர்வுகள் முக்கியமானவை. நம்பகமான ஒருவரிடம் பேசலாம்.",
        "general": "பகிர்ந்ததற்கு நன்றி. நான் பொதுவான நலவாழ்வு தகவல்களை மட்டுமே வழங்க முடியும்.",
        "crisis": "உடனே நம்பகமான பெரியவர் அல்லது தகுதியான நிபுணரிடம் பேசுங்கள். இந்தியாவில் உடனடி ஆபத்து இருந்தால் 112 எண்ணை அழைக்கவும்."
    },
    "हिन्दी": {
        "welcome": "MindCare AI में आपका स्वागत है।",
        "stress": "थोड़ा विराम लें और एक समय में एक छोटा काम करें।",
        "sleep": "नियमित सोने का समय आराम में मदद कर सकता है।",
        "study": "पढ़ाई को छोटे हिस्सों में बाँटें और विराम लें।",
        "sad": "आपकी भावनाएँ महत्वपूर्ण हैं। किसी भरोसेमंद व्यक्ति से बात करें।",
        "general": "साझा करने के लिए धन्यवाद। मैं सामान्य जानकारी दे सकता हूँ, निदान नहीं।",
        "crisis": "किसी भरोसेमंद बड़े व्यक्ति या पेशेवर से संपर्क करें। भारत में तत्काल खतरे पर 112 पर कॉल करें।"
    },
    "తెలుగు": {
        "welcome": "MindCare AI కి స్వాగతం. మీ శ్రేయస్సు ముఖ్యం.",
        "stress": "కొద్దిసేపు విరామం తీసుకుని సౌకర్యంగా శ్వాసించండి.",
        "sleep": "క్రమమైన నిద్ర సమయం విశ్రాంతికి సహాయపడుతుంది.",
        "study": "చదువును చిన్న భాగాలుగా విభజించి విరామాలు తీసుకోండి.",
        "sad": "మీ భావాలు ముఖ్యం. నమ్మకమైన వ్యక్తితో మాట్లాడండి.",
        "general": "పంచుకున్నందుకు ధన్యవాదాలు. నేను సాధారణ సమాచారం మాత్రమే అందించగలను.",
        "crisis": "నమ్మకమైన పెద్దవారిని లేదా నిపుణుడిని సంప్రదించండి. భారతదేశంలో తక్షణ ప్రమాదం ఉంటే 112కు కాల్ చేయండి."
    }
}

CRISIS_TERMS = [
    "suicide", "kill myself", "end my life",
    "hurt myself", "self harm", "want to die",
    "தற்கொலை", "आत्महत्या", "ఆత్మహత్య"
]


def chatbot_reply(message, language):
    q = message.lower()
    t = TEXT[language]

    if any(word in q for word in CRISIS_TERMS):
        return t["crisis"]

    if any(word in q for word in ["stress", "pressure", "tension", "மன அழுத்த", "तनाव", "ఒత్తిడి"]):
        return t["stress"]

    if any(word in q for word in ["sleep", "tired", "rest", "தூக்கம்", "नींद", "నిద్ర"]):
        return t["sleep"]

    if any(word in q for word in ["study", "focus", "படிப்பு", "पढ़ाई", "చదువు"]):
        return t["study"]

    if any(word in q for word in ["sad", "lonely", "upset", "வருத்த", "दुखी", "బాధ"]):
        return t["sad"]

    return t["general"]


# ================= PDF REPORT =================

def make_pdf_report(records):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    )
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("MindCare AI - Weekly Wellness Report", styles["Title"]),
        Spacer(1, 15),
        Paragraph(
            "Educational self-reflection report. Not a medical diagnosis.",
            styles["BodyText"]
        ),
        Spacer(1, 15)
    ]

    if records:
        data = [["Date", "Mood", "Stress", "Sleep", "Energy", "Focus"]]

        for item in records[-7:]:
            data.append([
                item.get("Date", ""),
                item.get("Mood", ""),
                item.get("Stress", ""),
                item.get("Sleep", ""),
                item.get("Energy", ""),
                item.get("Focus", "")
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#087f70")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8)
        ]))
        story.append(table)
    else:
        story.append(
            Paragraph("No assessment records available.", styles["BodyText"])
        )

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ================= FACE LANDMARK DETECTOR =================

def detect_face_landmarks(rgb_image):

    if not MEDIAPIPE_AVAILABLE:
        raise RuntimeError("MediaPipe is unavailable. Check requirements.txt.")

    mesh = mp.solutions.face_mesh
    drawing = mp.solutions.drawing_utils

    with mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as detector:

        result = detector.process(rgb_image)

    if not result.multi_face_landmarks:
        return None, None

    face = result.multi_face_landmarks[0]
    output = rgb_image.copy()

    drawing.draw_landmarks(
        image=output,
        landmark_list=face,
        connections=mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=drawing.DrawingSpec(
            color=(35, 220, 170),
            thickness=1,
            circle_radius=1
        )
    )

    drawing.draw_landmarks(
        image=output,
        landmark_list=face,
        connections=mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=drawing.DrawingSpec(
            color=(255, 190, 55),
            thickness=2,
            circle_radius=2
        )
    )

    points = face.landmark

    mouth_width = np.hypot(
        points[61].x - points[291].x,
        points[61].y - points[291].y
    )

    mouth_opening = np.hypot(
        points[13].x - points[14].x,
        points[13].y - points[14].y
    )

    ratio = mouth_opening / max(mouth_width, 0.0001)

    if ratio > 0.12:
        label = "Open-mouth expression"
        emoji = "😮"
        note = "The mouth appears open. This may happen while speaking or reacting."
    else:
        label = "Relatively closed-mouth expression"
        emoji = "🙂"
        note = "The mouth appears relatively closed. This alone cannot identify a mood."

    return output, (label, emoji, note)


# ================= SIDEBAR =================

st.sidebar.markdown("## 💚 MindCare AI")
st.sidebar.caption("Pause • Reflect • Recharge")

language = st.sidebar.selectbox("🌐 Select Language", LANGUAGES)

page = st.sidebar.radio(
    "✨ Explore MindCare AI",
    [
        "😊 Face Expression Studio",
        "🏡 Welcome Home",
        "📝 Wellbeing Assessment",
        "💬 AI Support Assistant",
        "📅 Daily Mood Tracker",
        "🧩 Mindful Mini Games",
        "🧘 Stress Relief Studio",
        "🌱 Personalised Suggestions",
        "🎙️ Voice Assistant",
        "📊 Wellbeing Insights",
        "🤖 AI / ML Playground",
        "📄 Weekly Wellness Report",
        "❤️ Crisis Support",
        "🤝 Support Resources"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Educational wellbeing prototype")
st.sidebar.caption("Not a medical diagnosis")


# ================= FACE EXPRESSION STUDIO =================

if page == "😊 Face Expression Studio":

    st.markdown("""
    <div class="hero">
        <h1>😊 AI Face Expression Studio</h1>
        <p>Capture a selfie and explore connected facial landmarks.</p>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "Facial appearance cannot reliably reveal someone's actual mood. "
        "This demo observes visible facial cues only; it does not diagnose "
        "mental health or identify emotions."
    )

    selfie = st.camera_input("📸 Take your selfie")

    if selfie is not None:

        image = Image.open(selfie).convert("RGB")
        rgb = np.array(image)

        try:
            with st.spinner("✨ Mapping facial landmarks..."):
                mesh_image, observation = detect_face_landmarks(rgb)

            if mesh_image is None:
                st.warning("No face detected. Try a clear, front-facing selfie.")

            else:
                col1, col2 = st.columns(2)

                col1.image(
                    rgb,
                    caption="📸 Original selfie",
                    use_container_width=True
                )

                col2.image(
                    mesh_image,
                    caption="🔵 Connected facial landmark mesh",
                    use_container_width=True
                )

                label, emoji, explanation = observation

                st.markdown(
                    f"<div class='panel'><h2 style='text-align:center'>"
                    f"{emoji} {label}</h2><p style='text-align:center'>"
                    f"{explanation}</p></div>",
                    unsafe_allow_html=True
                )

                st.success("Facial landmarks detected successfully!")

        except Exception as error:
            st.error("Face detector could not run. Check deployment dependencies.")
            st.caption(str(error))


# ================= WELCOME HOME =================

elif page == "🏡 Welcome Home":

    st.markdown("""
    <div class="hero">
        <h1>💚 Welcome to MindCare AI</h1>
        <p>Your friendly assistant for reflection, encouragement
        and everyday wellbeing.</p>
        <p>✨ Pause • Reflect • Recharge ✨</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    col1.metric("📝 Assessments", len(st.session_state.history))
    col2.metric("📅 Mood check-ins", len(st.session_state.mood_log))
    col3.metric("⭐ Mindful points", st.session_state.game_points)

    st.markdown("### ✨ Your wellbeing toolkit")

    features = [
        ("😊", "Face Expression Studio", "Explore facial landmarks."),
        ("🧩", "Mindful Mini Games", "Try gentle interactive activities."),
        ("🧘", "Stress Relief Studio", "Explore calming exercises."),
        ("💬", "AI Support Assistant", "Get general supportive information."),
        ("📅", "Daily Mood Tracker", "Record a daily reflection."),
        ("📄", "Weekly Wellness Report", "Review your recent reflections.")
    ]

    columns = st.columns(3)

    for index, (emoji, title, description) in enumerate(features):
        with columns[index % 3]:
            st.markdown(
                f"<div class='feature'><h2>{emoji}</h2>"
                f"<h4>{title}</h4><p>{description}</p></div>",
                unsafe_allow_html=True
            )

    st.info(TEXT[language]["welcome"])


# ================= WELLBEING ASSESSMENT =================

elif page == "📝 Wellbeing Assessment":

    st.title("📝 Wellbeing Assessment")
    st.write("Reflect on your recent experiences. There are no right or wrong answers.")

    with st.form("assessment_form"):

        mood = st.select_slider(
            "How would you describe your mood?",
            ["Very low", "Low", "Okay", "Good", "Very good"]
        )

        stress = st.select_slider(
            "How manageable has daily stress felt?",
            ["Very difficult", "Difficult", "Moderate", "Manageable", "Very manageable"]
        )

        sleep = st.select_slider(
            "How has your sleep been?",
            ["Very poor", "Poor", "Fair", "Good", "Very good"]
        )

        energy = st.select_slider(
            "How has your energy been?",
            ["Very low", "Low", "Average", "Good", "High"]
        )

        focus = st.select_slider(
            "How has your concentration been?",
            ["Very difficult", "Difficult", "Average", "Good", "Very good"]
        )

        activity = st.selectbox(
            "How often do you do activities you enjoy?",
            ["Daily", "Several times a week", "Sometimes", "Rarely"]
        )

        submitted = st.form_submit_button("💚 Save my reflection")

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

        st.success("Your reflection has been saved for this session.")
        st.info("These answers are reflections, not a diagnosis.")

        if mood in ["Very low", "Low"]:
            st.write("🌿 Consider speaking with someone you trust.")
        elif stress in ["Very difficult", "Difficult"]:
            st.write("🌿 Try taking a comfortable break and choosing one small task.")
        else:
            st.write("🌿 Continue the routines and activities that support you.")


# ================= AI SUPPORT ASSISTANT =================

elif page == "💬 AI Support Assistant":

    st.title("💬 MindCare Support Assistant")

    st.caption(
        "A multilingual, rule-based educational assistant. "
        "It is not a clinical AI chatbot."
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("What would you like to talk about?")

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        response = chatbot_reply(user_input, language)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()


# ================= DAILY MOOD TRACKER =================

elif page == "📅 Daily Mood Tracker":

    st.title("📅 Daily Mood Tracker")

    with st.form("mood_form"):

        selected_date = st.date_input("Date", date.today())

        mood = st.selectbox(
            "Which word describes today?",
            ["Happy", "Calm", "Okay", "Stressed", "Sad", "Tired", "Mixed", "Prefer not to say"]
        )

        note = st.text_area("Optional reflection")

        save = st.form_submit_button("Save mood check-in")

    if save:

        st.session_state.mood_log.append({
            "Date": str(selected_date),
            "Mood": mood,
            "Note": note
        })

        st.success("Mood check-in saved for this session.")

    if st.session_state.mood_log:

        mood_df = pd.DataFrame(st.session_state.mood_log)

        st.dataframe(mood_df, use_container_width=True)

        st.bar_chart(mood_df["Mood"].value_counts())


# ================= MINDFUL MINI GAMES =================

elif page == "🧩 Mindful Mini Games":

    st.title("🧩 Mindful Mini Games")

    st.write("Enjoy gentle activities for attention and reflection.")

    game = st.radio(
        "Choose a mini game",
        [
            "🌈 Colour Check-in",
            "🔎 Observation Challenge",
            "💛 Gratitude Prompt",
            "🧠 Memory Challenge"
        ]
    )

    if game == "🌈 Colour Check-in":

        colour = st.radio(
            "Choose a colour that represents how you feel",
            ["🟢 Green", "🔵 Blue", "🟡 Yellow", "🟣 Purple", "🟠 Orange"]
        )

        if st.button("Submit colour choice"):
            st.session_state.game_points += 1
            st.success("✨ Thank you for checking in! +1 point")

    elif game == "🔎 Observation Challenge":

        prompts = [
            "Find three circular objects around you.",
            "Notice two different sounds.",
            "Find three objects with different textures.",
            "Notice one detail you had not seen before."
        ]

        st.write(random.choice(prompts))

        if st.button("Complete challenge"):
            st.session_state.game_points += 1
            st.success("🔎 Well observed! +1 point")

    elif game == "💛 Gratitude Prompt":

        prompts = [
            "Name one small thing that made today easier.",
            "Think of someone who has supported you.",
            "Recall a moment you enjoyed recently.",
            "What is one thing you look forward to?"
        ]

        st.write(random.choice(prompts))
        st.text_area("Optional reflection")

        if st.button("Complete gratitude activity"):
            st.session_state.game_points += 1
            st.success("💛 Thank you for reflecting! +1 point")

    else:

        if st.button("Generate memory sequence"):

            st.session_state.memory_sequence = [
                random.choice(["🍀", "🌟", "🌻", "🌈", "💧", "🦋"])
                for _ in range(4)
            ]

        sequence = st.session_state.memory_sequence

        if sequence:

            st.markdown("### " + "  ".join(sequence))

            answer = st.text_input("Enter the four emojis in the same order")

            if st.button("Check sequence"):

                if answer.replace(" ", "") == "".join(sequence):
                    st.session_state.game_points += 1
