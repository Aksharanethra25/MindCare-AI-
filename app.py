import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from sklearn.cluster import KMeans
from PIL import Image
import cv2
import mediapipe as mp
import io
import tempfile
import os

st.set_page_config(page_title="MindCare AI", page_icon="💚", layout="wide")

# -------------------- SESSION DATA --------------------
for key, default in {
    "history": [],
    "messages": [],
    "mood_log": [],
    "activities": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------- HELPERS --------------------
LANGUAGES = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi",
    "తెలుగు": "te",
}

TEXT = {
    "English": {
        "welcome": "Welcome. Your wellbeing matters, and small steps count.",
        "stress": "Try a gentle pause, slow breathing, or one manageable task at a time.",
        "sleep": "A steady sleep routine and a calm wind-down can support rest.",
        "study": "Break your work into smaller tasks and take short, regular breaks.",
        "sad": "Your feelings deserve care. Consider speaking with a trusted adult or counsellor.",
        "general": "Thank you for sharing. I can offer general wellbeing information, not a diagnosis.",
        "crisis": "I'm glad you reached out. Please contact a trusted adult or qualified professional now. If anyone is in immediate danger in India, call 112 or go to the nearest emergency department. Stay with a trusted person while getting help.",
        "recommend": "Choose one small, realistic activity that feels comfortable. You could take a short break, listen to calming music, write down a thought, or talk with someone you trust.",
    },
    "தமிழ்": {
        "welcome": "வரவேற்கிறோம். உங்கள் நலன் முக்கியம். சிறிய நல்ல முயற்சிகளும் உதவும்.",
        "stress": "சிறிது ஓய்வு எடுத்து மெதுவாக சுவாசிக்கவும். ஒரு சிறிய பணியை மட்டும் முதலில் செய்யுங்கள்.",
        "sleep": "தினமும் ஒரே நேரத்தில் தூங்கும் பழக்கம் ஓய்வுக்கு உதவலாம்.",
        "study": "படிப்பைச் சிறிய பகுதிகளாகப் பிரித்து இடையில் ஓய்வு எடுக்கவும்.",
        "sad": "உங்கள் உணர்வுகள் முக்கியமானவை. நம்பகமான பெரியவர் அல்லது ஆலோசகரிடம் பேசலாம்.",
        "general": "பகிர்ந்ததற்கு நன்றி. நான் பொதுவான நலவாழ்வு தகவல்களை மட்டுமே வழங்க முடியும்.",
        "crisis": "நீங்கள் உதவி கேட்பது முக்கியம். உடனே நம்பகமான பெரியவர் அல்லது தகுதியான நிபுணரிடம் பேசுங்கள். இந்தியாவில் உடனடி ஆபத்து இருந்தால் 112 எண்ணை அழைக்கவும் அல்லது அருகிலுள்ள அவசர சிகிச்சை மையத்திற்குச் செல்லவும்.",
        "recommend": "உங்களுக்கு வசதியான ஒரு சிறிய செயலைத் தேர்வு செய்யுங்கள்: ஓய்வு, அமைதியான இசை, எண்ணங்களை எழுதுதல் அல்லது நம்பகமான ஒருவரிடம் பேசுதல்.",
    },
    "हिन्दी": {
        "welcome": "आपका स्वागत है। आपका स्वास्थ्य और अच्छा महसूस करना महत्वपूर्ण है।",
        "stress": "थोड़ा विराम लें, धीरे सांस लें और एक समय में एक छोटा काम करें।",
        "sleep": "नियमित सोने का समय आराम में मदद कर सकता है।",
        "study": "पढ़ाई को छोटे हिस्सों में बाँटें और बीच-बीच में विराम लें।",
        "sad": "आपकी भावनाएँ महत्वपूर्ण हैं। किसी भरोसेमंद बड़े व्यक्ति या काउंसलर से बात करें।",
        "general": "साझा करने के लिए धन्यवाद। मैं सामान्य जानकारी दे सकता हूँ, निदान नहीं।",
        "crisis": "कृपया अभी किसी भरोसेमंद बड़े व्यक्ति या योग्य पेशेवर से संपर्क करें। भारत में तत्काल खतरे की स्थिति में 112 पर कॉल करें या नजदीकी आपातकालीन सेवा लें।",
        "recommend": "एक छोटा और सहज कदम चुनें—थोड़ा आराम, शांत संगीत, लिखना या भरोसेमंद व्यक्ति से बात करना।",
    },
    "తెలుగు": {
        "welcome": "స్వాగతం. మీ శ్రేయస్సు ముఖ్యం. చిన్న మంచి అడుగులు కూడా సహాయపడతాయి.",
        "stress": "కొద్దిసేపు విరామం తీసుకుని నెమ్మదిగా శ్వాసించండి. ఒక్క చిన్న పనితో ప్రారంభించండి.",
        "sleep": "క్రమమైన నిద్ర సమయం విశ్రాంతికి సహాయపడుతుంది.",
        "study": "చదువును చిన్న భాగాలుగా విభజించి మధ్యలో విరామాలు తీసుకోండి.",
        "sad": "మీ భావాలు ముఖ్యం. నమ్మకమైన పెద్దవారితో లేదా కౌన్సిలర్‌తో మాట్లాడండి.",
        "general": "పంచుకున్నందుకు ధన్యవాదాలు. నేను సాధారణ సమాచారం మాత్రమే అందించగలను; నిర్ధారణ చేయలేను.",
        "crisis": "దయచేసి వెంటనే నమ్మకమైన పెద్దవారిని లేదా అర్హత కలిగిన నిపుణుడిని సంప్రదించండి. భారతదేశంలో తక్షణ ప్రమాదం ఉంటే 112కు కాల్ చేయండి లేదా సమీప అత్యవసర సేవను సంప్రదించండి.",
        "recommend": "మీకు సౌకర్యంగా ఉండే చిన్న పనిని ఎంచుకోండి: విరామం, ప్రశాంతమైన సంగీతం, రాయడం లేదా నమ్మకమైన వ్యక్తితో మాట్లాడడం.",
    },
}

CRISIS_TERMS = [
    "suicide", "kill myself", "end my life", "hurt myself",
    "self harm", "can't stay safe", "want to die",
    "தற்கொலை", "உயிரை மாய்த்துக்", "என்னை காயப்படுத்த",
    "आत्महत्या", "खुद को नुकसान", "मरना चाहता",
    "ఆత్మహత్య", "నన్ను నేను గాయపరచ"
]

def chatbot_reply(message, language):
    q = message.lower()
    t = TEXT[language]
    if any(term in q for term in CRISIS_TERMS):
        return t["crisis"]
    if any(w in q for w in ["stress", "pressure", "overwhelmed", "tension", "மன அழுத்த", "तनाव", "ఒత్తిడి"]):
        return t["stress"]
    if any(w in q for w in ["sleep", "tired", "rest", "தூக்கம்", "नींद", "నిద్ర"]):
        return t["sleep"]
    if any(w in q for w in ["study", "focus", "concentration", "படிப்பு", "पढ़ाई", "చదువు"]):
        return t["study"]
    if any(w in q for w in ["sad", "lonely", "upset", "வருத்த", "दुखी", "బాధ"]):
        return t["sad"]
    return t["general"]

def make_pdf_report(records):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("MindCare AI - Weekly Wellness Reflection", styles["Title"]),
        Spacer(1, 8),
        Paragraph("Educational self-reflection report. This is not a medical assessment or diagnosis.", styles["BodyText"]),
        Spacer(1, 12),
    ]
    if records:
        data = [["Date", "Mood", "Stress", "Sleep", "Energy", "Focus"]]
        for r in records[-7:]:
            data.append([r.get("Date", ""), r.get("Mood", ""), r.get("Stress", ""), r.get("Sleep", ""), r.get("Energy", ""), r.get("Focus", "")])
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#087f70")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(table)
    else:
        story.append(Paragraph("No assessment records are available yet. Complete a wellbeing assessment to populate this report.", styles["BodyText"]))
    story += [Spacer(1, 12), Paragraph("Supportive reminder: choose one manageable step and reach out to someone you trust when you need support.", styles["BodyText"])]
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# -------------------- SIDEBAR --------------------
st.sidebar.title("💚 MindCare AI")
st.sidebar.caption("Your Wellbeing Companion")
language = st.sidebar.selectbox("🌐 Language / மொழி", list(LANGUAGES.keys()))
page = st.sidebar.radio("Navigation", [
    "Dashboard", "Wellbeing Assessment", "AI Support Assistant",
    "Daily Mood Tracker", "Stress Relief Assistant",
    "Personalised Recommendations", "Face Expression Detector",
    "Voice Assistant", "Wellbeing Insights", "AI / ML Demonstration",
    "Weekly Wellness Report", "Crisis Support System", "Support Resources"
])
st.sidebar.divider()
st.sidebar.caption("Educational prototype | Not a medical diagnosis")

# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    st.title("💚 MindCare AI")
    st.subheader("Mental Wellness & Support Platform")
    st.success(TEXT[language]["welcome"])
    st.info("A privacy-conscious educational platform for self-reflection and supportive resources.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Assessments completed", len(st.session_state.history))
    c2.metric("Mood check-ins", len(st.session_state.mood_log))
    c3.metric("Support conversations", len(st.session_state.messages))
    st.divider()
    st.subheader("Explore your wellbeing space")
    cards = [
        ("📝", "Wellbeing Assessment", "Reflect on mood, sleep, stress and energy."),
        ("📅", "Daily Mood Tracker", "Record a voluntary daily check-in."),
        ("😊", "Face Expression Detector", "Explore facial landmarks and visible cues."),
        ("🎙️", "Voice Assistant", "Record audio or use typed support."),
        ("🧘", "Stress Relief Assistant", "Try a short grounding or breathing activity."),
        ("📊", "Weekly Wellness Report", "Review your recent reflections.")
    ]
    cols = st.columns(3)
    for i, (emoji, title, desc) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"### {emoji} {title}")
            st.caption(desc)
    st.caption("Your wellbeing matters. Take things one step at a time.")

# -------------------- ASSESSMENT --------------------
elif page == "Wellbeing Assessment":
    st.title("📝 Wellbeing Assessment")
    st.write("Reflect on your recent experiences. There are no right or wrong answers.")
    with st.form("assessment_form"):
        mood = st.select_slider("How would you describe your mood?", options=["Very low", "Low", "Okay", "Good", "Very good"])
        stress = st.select_slider("How manageable has your daily stress felt?", options=["Very difficult", "Difficult", "Moderate", "Manageable", "Very manageable"])
        sleep = st.select_slider("How has your sleep been?", options=["Very poor", "Poor", "Fair", "Good", "Very good"])
        energy = st.select_slider("How has your energy been?", options=["Very low", "Low", "Average", "Good", "High"])
        focus = st.select_slider("How has your concentration been?", options=["Very difficult", "Difficult", "Average", "Good", "Very good"])
        activity = st.selectbox("How often do you take part in activities you enjoy?", ["Daily", "Several times a week", "Sometimes", "Rarely"])
        submitted = st.form_submit_button("Submit Assessment")
    if submitted:
        record = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Mood": mood, "Stress": stress, "Sleep": sleep, "Energy": energy, "Focus": focus, "Activity": activity}
        st.session_state.history.append(record)
        st.success("Your assessment has been completed!")
        st.json(record)
        st.info("These responses are reflections, not a diagnosis or a measure of clinical risk.")
        st.markdown("### 💚 A supportive suggestion")
        if mood in ["Very low", "Low"]:
            st.write("Consider talking with someone you trust about how you have been feeling.")
        elif stress in ["Very difficult", "Difficult"]:
            st.write("Try taking a short break and identifying one manageable task at a time.")
        elif sleep in ["Very poor", "Poor"]:
            st.write("A consistent bedtime routine may help. Consider discussing ongoing sleep difficulties with a healthcare professional.")
        else:
            st.write("Consider continuing activities and routines that help you feel supported.")

# -------------------- CHATBOT --------------------
elif page == "AI Support Assistant":
    st.title("💬 MindCare Multilingual Support Assistant")
    st.caption("Choose a language in the sidebar. This is a simple rule-based educational assistant, not a clinical chatbot.")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = chatbot_reply(user_input, language)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

# -------------------- DAILY MOOD TRACKER --------------------
elif page == "Daily Mood Tracker":
    st.title("📅 Daily Mood Tracker")
    st.write("Record how you feel today. This is a personal reflection, not a score or diagnosis.")
    with st.form("daily_mood_form"):
        selected_date = st.date_input("Date", value=date.today())
        mood = st.selectbox("Choose a mood label", ["Happy", "Calm", "Okay", "Stressed", "Sad", "Tired", "Other"])
        note = st.text_area("Optional note (avoid entering private identifying information)")
        save = st.form_submit_button("Save mood check-in")
    if save:
        st.session_state.mood_log.append({"Date": str(selected_date), "Mood": mood, "Note": note})
        st.success("Your check-in was added to this session.")
    if st.session_state.mood_log:
        mood_df = pd.DataFrame(st.session_state.mood_log)
        st.dataframe(mood_df, use_container_width=True)
        st.bar_chart(mood_df["Mood"].value_counts())

# -------------------- STRESS RELIEF --------------------
elif page == "Stress Relief Assistant":
    st.title("🧘 Stress Relief Assistant")
    st.write("Choose a gentle activity. Stop whenever you feel uncomfortable.")
    activity = st.radio("Select an activity", ["Calm breathing", "5-4-3-2-1 grounding", "Thought check-in", "Short study reset"])
    if activity == "Calm breathing":
        st.markdown("### 🌿 A gentle breathing pause")
        st.write("Breathe in comfortably for 4 counts, then breathe out gently for 4 counts. Repeat a few times at your own pace. Do not force or hold your breath.")
    elif activity == "5-4-3-2-1 grounding":
        st.markdown("### 🌱 Notice your surroundings")
        st.write("Name 5 things you can see, 4 things you can feel, 3 things you can hear, 2 things you can smell, and 1 thing you can taste. Skip anything that does not feel comfortable.")
    elif activity == "Thought check-in":
        thought = st.text_area("What is on your mind? (Optional)")
        st.caption("You do not need to share this with the app. You can simply reflect privately.")
    else:
        st.write("Choose one small task, work on it for a short period, then take a comfortable break.")
    if st.button("Save activity as completed"):
        st.session_state.activities.append({"Date": str(date.today()), "Activity": activity})
        st.success("Activity recorded for this session.")

# -------------------- RECOMMENDATIONS --------------------
elif page == "Personalised Recommendations":
    st.title("💡 Personalised Wellness Recommendations")
    st.write("Select what would be helpful today. These are general wellbeing ideas.")
    need = st.selectbox("What would you like support with?", ["Managing stress", "Building a sleep routine", "Study focus", "Feeling connected", "Taking a break", "Not sure"])
    suggestions = {
        "Managing stress": ["Break a task into smaller steps.", "Take a comfortable pause.", "Talk with someone you trust."],
        "Building a sleep routine": ["Try a consistent wind-down routine.", "Keep your sleep space comfortable.", "If sleep problems continue, discuss them with a healthcare professional."],
        "Study focus": ["Choose one clear task.", "Reduce distractions where possible.", "Take short breaks between study periods."],
        "Feeling connected": ["Send a message to someone you trust.", "Spend time with a supportive friend or family member.", "Consider a school or college counsellor."],
        "Taking a break": ["Stretch gently if comfortable.", "Listen to calming music.", "Step away from your screen for a little while."],
        "Not sure": [TEXT[language]["recommend"], "You can start with one small, manageable action."]
    }
    st.markdown("### 🌱 Suggestions")
    for item in suggestions[need]:
        st.write("✨ " + item)

# -------------------- FACE EXPRESSION DETECTOR --------------------
elif page == "Face Expression Detector":
    st.title("😊 AI Face Expression Detector")
    st.write("Take a selfie to view connected facial landmarks and a limited visible-expression observation.")
    st.info("Your camera photo is processed for this page. This demo does not identify a person's true feelings or diagnose mental health.")
    selfie = st.camera_input("📸 Take a selfie with your phone camera")
    if selfie is not None:
        try:
            image = Image.open(selfie).convert("RGB")
            image_array = np.array(image)
            with st.spinner("Mapping facial landmarks..."):
                face_mesh_module = mp.solutions.face_mesh
                drawing = mp.solutions.drawing_utils
                with face_mesh_module.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as detector:
                    result = detector.process(image_array)
                if result.multi_face_landmarks:
                    face = result.multi_face_landmarks[0]
                    output = image_array.copy()
                    drawing.draw_landmarks(
                        image=output, landmark_list=face,
                        connections=face_mesh_module.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=drawing.DrawingSpec(color=(0, 220, 170), thickness=1, circle_radius=1)
                    )
                    drawing.draw_landmarks(
                        image=output, landmark_list=face,
                        connections=face_mesh_module.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=drawing.DrawingSpec(color=(255, 190, 40), thickness=2, circle_radius=2)
                    )
                    points = face.landmark
                    mouth_width = np.hypot(points[61].x-points[291].x, points[61].y-points[291].y)
                    mouth_opening = np.hypot(points[13].x-points[14].x, points[13].y-points[14].y)
                    ratio = mouth_opening / max(mouth_width, 0.0001)
                    if ratio > 0.12:
                        observation, emoji = "Open-mouth expression", "😮"
                        explanation = "The mouth appears open in this image. This may occur while speaking or reacting."
                    else:
                        observation, emoji = "Relatively closed-mouth expression", "🙂"
                        explanation = "The mouth appears relatively closed. This cue alone cannot establish a mood."
                    c1, c2 = st.columns(2)
                    c1.image(image_array, caption="Original selfie", use_container_width=True)
                    c2.image(output, caption="Connected facial landmark mesh", use_container_width=True)
                    st.markdown(f"## {emoji} {observation}")
                    st.write(explanation)
                    st.success("Facial landmarks detected.")
                else:
                    st.warning("No face detected. Try a clear, front-facing selfie.")
        except Exception as e:
            st.error("The face detector could not run. Check the installed dependencies and try again.")
            st.caption(str(e))

# -------------------- VOICE ASSISTANT --------------------
elif page == "Voice Assistant":
    st.title("🎙️ MindCare Voice Assistant")
    st.write("Record a short voice note or type a message. Audio is not automatically transcribed in this prototype.")
    audio = st.audio_input("🎤 Record a voice note")
    if audio is not None:
        st.audio(audio)
        st.info("Your recording is available for playback in this session. Automatic speech-to-text is not enabled yet.")
    typed = st.text_input("Or type your message")
    if st.button("Get supportive response") and typed.strip():
        response = chatbot_reply(typed, language)
        st.success(response)
        st.caption("Spoken text-to-speech output is not enabled in this prototype.")
