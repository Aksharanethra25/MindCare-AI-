import streamlit as st
import pandas as pd
import numpy as np
import random
import io
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans

# Optional face landmark support
try:
    import mediapipe as mp
    FACE_AVAILABLE = True
except Exception:
    mp = None
    FACE_AVAILABLE = False

# Optional spoken output
try:
    from gtts import gTTS
    VOICE_AVAILABLE = True
except Exception:
    VOICE_AVAILABLE = False


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg,#f4f7ff,#effaf5,#fff5f8);
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(120deg,#12364b,#087f72,#40c49b);
    padding: 42px;
    border-radius: 28px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 12px 35px rgba(20,90,80,.15);
}

.hero h1 {
    color: white;
    font-family: 'Manrope',sans-serif;
    font-size: clamp(30px,5vw,48px);
    font-weight: 800;
}

.hero p {
    color: #e8fff7;
    font-size: 17px;
}

.card {
    background: rgba(255,255,255,.95);
    padding: 23px;
    border-radius: 20px;
    border: 1px solid #e5eee9;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(30,70,60,.05);
}

.feature-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #e6eee9;
    min-height: 150px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: #17675a;
    font-size: 18px;
}

.feature-card p {
    color: #71817d;
    font-size: 13px;
}

h1, h2, h3 {
    font-family: 'Manrope',sans-serif;
    color: #174f49;
}

div.stButton > button {
    border-radius: 13px;
    font-weight: 700;
    min-height: 42px;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg,#087f72,#36b995);
    color: white;
    border: none;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#e8f7f0,#f0f0ff);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LANGUAGES
# ==================================================

LANG = {
    "English": {
        "welcome": "Welcome to MindCare AI",
        "tagline": "Your friendly space for reflection, encouragement and everyday wellbeing.",
        "home": "Welcome Home",
        "face": "Face Expression Studio",
        "assessment": "Wellbeing Assessment",
        "assistant": "AI Support Assistant",
        "mood": "Daily Mood Tracker",
        "games": "Mindful Mini Games",
        "stress": "Stress Relief Studio",
        "suggestions": "Personalised Suggestions",
        "voice": "Voice Assistant",
        "insights": "Wellbeing Insights",
        "playground": "AI/ML Playground",
        "report": "Weekly Wellness Report",
        "crisis": "Crisis Support",
        "resources": "Support Resources",
        "language": "Choose your language",
        "name": "Your name",
        "email": "Email address",
        "username": "Username",
        "password": "Password",
        "create": "Create account",
        "login": "Login",
        "logout": "Logout",
        "mood_question": "How are you feeling today?"
    },
    "தமிழ்": {
        "welcome": "MindCare AI-க்கு வரவேற்கிறோம்",
        "tagline": "உங்கள் நலனுக்காக சிந்திக்கவும் ஊக்கம் பெறவும் உதவும் இடம்.",
        "home": "முகப்பு",
        "face": "முக வெளிப்பாட்டு ஸ்டுடியோ",
        "assessment": "நலவாழ்வு மதிப்பீடு",
        "assistant": "AI ஆதரவு உதவியாளர்",
        "mood": "தினசரி மனநிலை பதிவு",
        "games": "மனநிறைவு சிறு விளையாட்டுகள்",
        "stress": "மன அழுத்த நிவாரணம்",
        "suggestions": "தனிப்பட்ட பரிந்துரைகள்",
        "voice": "குரல் உதவியாளர்",
        "insights": "நலவாழ்வு தகவல்கள்",
        "playground": "AI/ML பயிற்சி",
        "report": "வாராந்திர அறிக்கை",
        "crisis": "அவசர ஆதரவு",
        "resources": "ஆதரவு வளங்கள்",
        "language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "name": "உங்கள் பெயர்",
        "email": "மின்னஞ்சல்",
        "username": "பயனர் பெயர்",
        "password": "கடவுச்சொல்",
        "create": "கணக்கை உருவாக்கு",
        "login": "உள்நுழை",
        "logout": "வெளியேறு",
        "mood_question": "இன்று நீங்கள் எப்படி உணர்கிறீர்கள்?"
    },
    "മലയാളം": {
        "welcome": "MindCare AI-ലേക്ക് സ്വാഗതം",
        "tagline": "നിങ്ങളുടെ ക്ഷേമത്തിനും ആത്മപരിശോധനയ്ക്കുമുള്ള സൗഹൃദ ഇടം.",
        "home": "ഹോം",
        "face": "മുഖഭാവ സ്റ്റുഡിയോ",
        "assessment": "ക്ഷേമ വിലയിരുത്തൽ",
        "assistant": "AI സഹായ സഹായി",
        "mood": "ദൈനംദിന മാനസികാവസ്ഥ",
        "games": "മൈൻഡ്ഫുൾ മിനി ഗെയിമുകൾ",
        "stress": "സ്ട്രെസ് റിലീഫ് സ്റ്റുഡിയോ",
        "suggestions": "വ്യക്തിഗത നിർദ്ദേശങ്ങൾ",
        "voice": "വോയ്സ് അസിസ്റ്റന്റ്",
        "insights": "ക്ഷേമ വിവരങ്ങൾ",
        "playground": "AI/ML പ്ലേഗ്രൗണ്ട്",
        "report": "ആഴ്ചതോറുമുള്ള റിപ്പോർട്ട്",
        "crisis": "അടിയന്തര പിന്തുണ",
        "resources": "പിന്തുണാ വിഭവങ്ങൾ",
        "language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "name": "നിങ്ങളുടെ പേര്",
        "email": "ഇമെയിൽ",
        "username": "ഉപയോക്തൃനാമം",
        "password": "പാസ്‌വേഡ്",
        "create": "അക്കൗണ്ട് സൃഷ്ടിക്കുക",
        "login": "ലോഗിൻ",
        "logout": "ലോഗ്ഔട്ട്",
        "mood_question": "ഇന്ന് നിങ്ങൾക്ക് എങ്ങനെ തോന്നുന്നു?"
    },
    "తెలుగు": {
        "welcome": "MindCare AI కి స్వాగతం",
        "tagline": "మీ రోజువారీ శ్రేయస్సు కోసం స్నేహపూర్వక స్థలం.",
        "home": "హోమ్",
        "face": "ముఖ కవళికల స్టూడియో",
        "assessment": "శ్రేయస్సు అంచనా",
        "assistant": "AI సహాయకుడు",
        "mood": "రోజువారీ మూడ్ ట్రాకర్",
        "games": "మైండ్‌ఫుల్ చిన్న ఆటలు",
        "stress": "ఒత్తిడి ఉపశమన స్టూడియో",
        "suggestions": "వ్యక్తిగత సూచనలు",
        "voice": "వాయిస్ అసిస్టెంట్",
        "insights": "శ్రేయస్సు విశ్లేషణ",
        "playground": "AI/ML ప్లేగ్రౌండ్",
        "report": "వారపు నివేదిక",
        "crisis": "అత్యవసర సహాయం",
        "resources": "సహాయక వనరులు",
        "language": "భాషను ఎంచుకోండి",
        "name": "మీ పేరు",
        "email": "ఇమెయిల్",
        "username": "వినియోగదారు పేరు",
        "password": "పాస్‌వర్డ్",
        "create": "ఖాతా సృష్టించండి",
        "login": "లాగిన్",
        "logout": "లాగ్అవుట్",
        "mood_question": "ఈ రోజు మీకు ఎలా అనిపిస్తోంది?"
    },
    "हिन्दी": {
        "welcome": "MindCare AI में आपका स्वागत है",
        "tagline": "आपके रोज़मर्रा के स्वास्थ्य के लिए एक मित्रवत स्थान।",
        "home": "होम",
        "face": "फेस एक्सप्रेशन स्टूडियो",
        "assessment": "कल्याण मूल्यांकन",
        "assistant": "AI सहायता सहायक",
        "mood": "दैनिक मूड ट्रैकर",
        "games": "माइंडफुल मिनी गेम्स",
        "stress": "तनाव राहत स्टूडियो",
        "suggestions": "व्यक्तिगत सुझाव",
        "voice": "वॉयस असिस्टेंट",
        "insights": "कल्याण जानकारी",
        "playground": "AI/ML प्लेग्राउंड",
        "report": "साप्ताहिक रिपोर्ट",
        "crisis": "आपातकालीन सहायता",
        "resources": "सहायता संसाधन",
        "language": "अपनी भाषा चुनें",
        "name": "आपका नाम",
        "email": "ईमेल पता",
        "username": "उपयोगकर्ता नाम",
        "password": "पासवर्ड",
        "create": "खाता बनाएँ",
        "login": "लॉगिन",
        "logout": "लॉगआउट",
        "mood_question": "आज आप कैसा महसूस कर रहे हैं?"
    }
}


# ==================================================
# NAVIGATION ORDER
# ==================================================

NAV = [
    "home",
    "face",
    "assessment",
    "assistant",
    "mood",
    "games",
    "stress",
    "suggestions",
    "voice",
    "insights",
    "playground",
    "report",
    "crisis",
    "resources"
]


# ==================================================
# SESSION DATA
# ==================================================

defaults = {
    "language": "English",
    "page": "home",
    "logged_in": False,
    "users": {},
    "username": "",
    "display_name": "",
    "moods": [],
    "assessments": [],
    "activities": [],
    "chat": [],
    "emoji_sequence": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def save_mood(mood, note=""):
    st.session_state.moods.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood": mood,
        "note": note
    })


def save_assessment(data):
    st.session_state.assessments.append(data)


def save_activity(name, details):
    st.session_state.activities.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "activity": name,
        "details": details
    })


def chatbot_reply(message):
    msg = message.lower()

    if any(word in msg for word in ["stress", "stressed", "anxious", "கவலை", "तनाव", "ఒత్తిడి"]):
        return "It sounds like things may feel difficult today. Try a gentle pause, relax your shoulders and choose one small next step."

    if any(word in msg for word in ["sleep", "tired", "தூக்கம்", "नींद", "నిద్ర"]):
        return "A calm wind-down routine and a regular sleep schedule may help. What is one small change you could try tonight?"

    if any(word in msg for word in ["study", "exam", "college", "படிப்பு", "पढ़ाई", "చదువు"]):
        return "Choose one small study task, focus on it for a short period and then take a brief break."

    return "Thank you for sharing. Would you like to tell me a little more? We can explore one small, practical next step together."


# ==================================================
# LOGIN AND REGISTRATION
# ==================================================

def authentication_page(t):

    st.markdown("""
    <div class="hero">
        <h1>🌿 MindCare AI</h1>
        <p>Your personal space for reflection, encouragement and everyday wellbeing.</p>
        <h3 style="color:white">Pause • Reflect • Recharge ✨</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💚 Welcome! Create your personal account")

    st.info(
        "Demo account mode: accounts are stored only during the current app session. "
        "Do not use a real or reused password."
    )

    choice = st.radio(
        "Choose an option",
        ["Create Account", "Login"],
        horizontal=True
    )

    if choice == "Create Account":

        with st.form("register_form"):
            name = st.text_input(t["name"])
            email = st.text_input(t["email"])
            username = st.text_input(t["username"])
            password = st.text_input(t["password"], type="password")
            confirm = st.text_input("Confirm password", type="password")

            submitted = st.form_submit_button(
                t["create"], type="primary", use_container_width=True
            )

            if submitted:
                if not all([name, email, username, password, confirm]):
                    st.warning("Please complete all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 8:
                    st.error("Use at least 8 characters for the demo password.")
                elif username in st.session_state.users:
                    st.error("This username already exists.")
                else:
                    st.session_state.users[username] = {
                        "name": name,
                        "email": email,
                        "password": password
                    }
                    st.success("Account created! Select Login to continue.")

    else:

        with st.form("login_form"):
            username = st.text_input(t["username"])
            password = st.text_input(t["password"], type="password")

            submitted = st.form_submit_button(
                t["login"], type="primary", use_container_width=True
            )

            if submitted:
                user = st.session_state.users.get(username)

                if user and user["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.display_name = user["name"]
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")


# ==================================================
# WELCOME HOMEPAGE
# ==================================================

def home_page(t):

    name = st.session_state.display_name

    st.markdown(f"""
    <div class="hero">
        <h1>🌿 {t['welcome']}</h1>
        <p>{t['tagline']}</p>
        <h3 style="color:white">Pause • Reflect • Recharge ✨</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"## 👋 Hello, {name}!")

    st.markdown("""
    <div class="card">
        <h2>💚 What is MindCare AI?</h2>
        <p>
        MindCare AI is an educational wellbeing companion designed to help
        you reflect on your day, record your own feelings, explore mindful
        activities and discover helpful support resources.
        </p>
        <p>
        It offers self-reflection tools and learning activities.
        It is not a medical service or a mental health diagnosis tool.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✨ Explore your wellbeing toolkit")

    cards = [
        ("😊", t["face"], "Explore facial landmarks."),
        ("🌿", t["assessment"], "Reflect on sleep, energy and focus."),
        ("🤖", t["assistant"], "Chat with a supportive assistant."),
        ("📅", t["mood"], "Record your daily mood."),
        ("🎮", t["games"], "Try mindful mini-games."),
        ("🧘", t["stress"], "Explore calming activities."),
        ("✨", t["suggestions"], "Discover helpful suggestions."),
        ("🎙️", t["voice"], "Try the voice assistant."),
        ("📊", t["insights"], "View your recorded reflections."),
        ("🧪", t["playground"], "Explore machine learning."),
        ("📄", t["report"], "Prepare a weekly report."),
        ("🆘", t["crisis"], "Find support when needed."),
        ("📚", t["resources"], "Explore support resources.")
    ]

    cols = st.columns(3)

    for i, item in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <h2>{item[0]}</h2>
                <h3>{item[1]}</h3>
                <p>{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.success("Choose any feature from the sidebar to begin.")


# ==================================================
# FACE EXPRESSION STUDIO
# ==================================================

def face_page():

    st.markdown("## 😊 Face Expression Studio")

    st.write(
        "Take a selfie and explore facial landmarks. Facial appearance "
        "cannot reliably reveal someone's actual feelings or mental health."
    )

    photo = st.camera_input("📸 Take your selfie")

    if photo:

        image = Image.open(photo).convert("RGB")

        if FACE_AVAILABLE:

            try:
                mesh_module = mp.solutions.face_mesh

                with mesh_module.FaceMesh(
                    static_image_mode=True,
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5
                ) as face_mesh:

                    result = face_mesh.process(np.array(image))

                if result.multi_face_landmarks:

                    annotated = image.copy()
                    draw = ImageDraw.Draw(annotated)

                    width, height = annotated.size

                    for face in result.multi_face_landmarks:
                        for point in face.landmark:
                            px = int(point.x * width)
                            py = int(point.y * height)

                            draw.ellipse(
                                (px - 2, py - 2, px + 2, py + 2),
                                fill="#00E5A8"
                            )

                    st.image(
                        annotated,
                        caption="Facial landmark points",
                        use_container_width=True
                    )

                    st.success("Facial landmarks detected.")

                else:
                    st.warning("No face landmarks detected. Try another photo.")

            except Exception:
                st.warning("Face landmark processing is unavailable.")

        else:
            st.image(image, caption="Your selfie", use_container_width=True)
            st.info(
                "Face landmark support is unavailable in this deployment. "
                "The other features are still available."
            )

    st.markdown("### 💭 How are you feeling?")

    feeling = st.selectbox(
        "Choose your own feeling",
        ["Happy", "Calm", "Okay", "Tired", "Worried", "Stressed", "Unsure"]
    )

    if st.button("Save my feeling"):
        save_mood(feeling, "Self-reported check-in")
        st.success("Your check-in has been saved for this session.")


# ==================================================
# WELLBEING ASSESSMENT
# ==================================================

def assessment_page():

    st.markdown("## 🌿 Wellbeing Assessment")

    st.caption("A personal reflection tool, not a clinical assessment.")

    with st.form("wellbeing_form"):

        mood = st.select_slider(
            "How would you describe your mood?",
            options=["Very low", "Low", "Okay", "Good", "Very good"]
        )

        stress = st.slider("How stressful has today felt?", 0, 10, 5)
        sleep = st.slider("How restful was your sleep?", 0, 10, 5)
        energy = st.slider("How is your energy today?", 0, 10, 5)
        focus = st.slider("How is your focus today?", 0, 10, 5)

        activity = st.selectbox(
            "Your activity today",
            ["Not yet", "A little", "Some", "Quite a bit"]
        )

        notes = st.text_area("Optional reflection")

        submitted = st.form_submit_button(
            "Save my reflection", type="primary"
        )

    if submitted:

        data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mood": mood,
            "stress": stress,
            "sleep": sleep,
            "energy": energy,
            "focus": focus,
            "activity": activity,
            "notes": notes
        }

        save_assessment(data)
        st.success("Your reflection has been saved.")


# ==================================================
# AI SUPPORT ASSISTANT
# ==================================================

def assistant_page():

    st.markdown("## 🤖 AI Support Assistant")

    st.caption(
        "Educational support only. This is not a therapist or emergency service."
    )

    for message in st.session_state.chat:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("What would you like to talk about?")

    if prompt:

        st.session_state.chat.append({
            "role": "user",
            "content": prompt
        })

        reply = chatbot_reply(prompt)

        st.session_state.chat.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()


# ==================================================
# DAILY MOOD TRACKER
# ==================================================

def mood_page():

    st.markdown("## 📅 Daily Mood Tracker")

    mood = st.selectbox(
        "How are you feeling today?",
        ["Happy", "Calm", "Motivated", "Okay", "Tired", "Worried", "Stressed"]
    )

    note = st.text_area("Write a short note (optional)")

    if st.button("Save mood check-in", type="primary"):

        save_mood(mood, note)
        st.success("Mood saved.")

    if st.session_state.moods:

        st.markdown("### Recent mood check-ins")

        df = pd.DataFrame(st.session_state.moods)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# MINDFUL MINI GAMES
# ==================================================

def games_page():

    st.markdown("## 🎮 Mindful Mini Games")

    game = st.selectbox(
        "Choose a mini-game",
        [
            "Colour Check-in",
            "Gratitude Moment",
            "Observation Challenge",
            "Emoji Memory"
        ]
    )

    if game == "Colour Check-in":

        st.markdown("### 🎨 Choose your colour")

        colour = st.radio(
            "Which colour represents your current moment?",
            ["💚 Green", "💙 Blue", "💛 Yellow", "💜 Purple", "🧡 Orange"]
        )

        if st.button("Save colour"):
            save_activity("Colour Check-in", colour)
            st.success("Your choice has been recorded.")

    elif game == "Gratitude Moment":

        st.markdown("### 🌻 One thing you appreciated today")

        note = st.text_area("My gratitude note")

        if st.button("Save gratitude note"):

            if note.strip():
                save_activity("Gratitude", note)
                st.success("Your note has been saved.")

    elif game == "Observation Challenge":

        st.markdown("### 👀 Notice your surroundings")

        if st.button("Show challenge"):

            st.write(
                "Find something colourful, something with a pattern, "
                "something soft, something that makes a sound, and "
                "something you had not noticed before."
            )

    else:

        if st.button("Generate emoji sequence"):

            st.session_state.emoji_sequence = random.sample(
                ["🌈", "🌻", "🌙", "🍀", "⭐", "🦋", "🌊"],
                4
            )

        if st.session_state.emoji_sequence:

            st.markdown("### 🧠 Remember this sequence")

            st.title("  ".join(st.session_state.emoji_sequence))

            st.caption("A casual memory activity, not a test.")


# ==================================================
# STRESS RELIEF STUDIO
# ==================================================

def stress_page():

    st.markdown("## 🧘 Stress Relief Studio")

    activity = st.selectbox(
        "Choose an activity",
        [
            "Breathing Pause",
            "Grounding Exercise",
            "Study Reset",
            "Positive Reflection"
        ]
    )

    if activity == "Breathing Pause":

        st.markdown("### 🌬️ Gentle breathing pause")

        st.write(
            "Breathe in comfortably and breathe out slowly. "
            "Repeat at your own comfortable pace. Do not force or hold your breath."
        )

    elif activity == "Grounding Exercise":

        st.markdown("### 🌱 Notice your surroundings")

        st.write(
            "Notice a few things you can see, hear and feel around you. "
            "Take your time."
        )

    elif activity == "Study Reset":

        st.markdown("### 📚 Study reset")

        st.write(
            "1. Choose one small task.\n"
            "2. Keep the materials you need nearby.\n"
            "3. Work for a short, comfortable period.\n"
            "4. Take a brief break."
        )

    else:

        st.markdown("### 💚 Positive reflection")

        thought = st.text_area(
            "What is one thing you handled well today?"
        )

        if st.button("Save reflection"):

            if thought.strip():
                save_activity("Positive Reflection", thought)
                st.success("Reflection saved.")


# ==================================================
# PERSONALISED SUGGESTIONS
# ==================================================

def suggestions_page():

    st.markdown("## ✨ Personalised Suggestions")

    need = st.selectbox(
        "What would you like support with?",
        [
            "Study focus",
            "Relaxation",
            "Sleep routine",
            "Daily motivation",
            "Healthy habits"
        ]
    )

    suggestions = {
        "Study focus": [
            "Choose one small study goal.",
            "Keep distractions away during a short focus session.",
            "Take a brief break between tasks."
        ],
        "Relaxation": [
            "Try a comfortable breathing pause.",
            "Listen to calm music if you enjoy it.",
            "Notice your surroundings for a few moments."
        ],
        "Sleep routine": [
            "Try keeping a regular bedtime.",
            "Create a calm wind-down routine.",
            "Make your sleeping environment comfortable."
        ],
        "Daily motivation": [
            "Write down one achievable goal.",
            "Recognise small steps you complete.",
            "Ask someone you trust for encouragement."
        ],
        "Healthy habits": [
            "Start with one manageable habit.",
            "Connect it to an existing daily routine.",
            "Notice your progress without judging yourself."
        ]
    }

    for item in suggestions[need]:
        st.markdown(f"- 🌿 {item}")


# ==================================================
# VOICE ASSISTANT
# ==================================================

def voice_page():

    st.markdown("## 🎙️ Voice Assistant")

    audio = st.audio_input("Record your message")

    if audio:
        st.audio(audio)

        st.info(
            "Your recording is available above. Automatic speech transcription "
            "is not included. You can type the message below."
        )

    typed = st.text_input("Or type your message")

    if st.button("Get response"):

        if typed.strip():

            reply = chatbot_reply(typed)

            st.success(reply)

            if VOICE_AVAILABLE:

                language_codes = {
                    "English": "en",
                    "தமிழ்": "ta",
                    "മലയാളം": "ml",
                    "తెలుగు": "te",
                    "हिन्दी": "hi"
                }

                try:

                    speech = gTTS(
                        text=reply,
                        lang=language_codes[st.session_state.language]
                    )

                    buffer = io.BytesIO()
                    speech.write_to_fp(buffer)
                    buffer.seek(0)

                    st.audio(buffer, format="audio/mp3")

                except Exception:
                    st.info("Spoken response is temporarily unavailable.")

        else:
            st.warning("Please type a message first.")


# ==================================================
# WELLBEING INSIGHTS
# ==================================================

def insights_page():

    st.markdown("## 📊 Wellbeing Insights")

    if not st.session_state.assessments:

        st.info("Complete an assessment to see your insights.")
        return

    df = pd.DataFrame(st.session_state.assessments)

    columns = ["stress", "sleep", "energy", "focus"]

    st.markdown("### Your recorded reflections")

    st.line_chart(df[columns])

    st.caption(
        "These charts show your recorded reflections, not medical measurements "
        "or predictions."
    )


# ==================================================
# AI / ML PLAYGROUND
# ==================================================

def playground_page():

    st.markdown("## 🧪 AI/ML Playground")

    st.write(
        "Explore a simple K-Means clustering demonstration using sample data."
    )

    data = pd.DataFrame({
        "Study Hours": [1, 2, 3, 4, 5, 6, 7, 8],
        "Sleep Hours": [8, 7, 8, 6, 7, 6, 5, 6],
        "Activity Level": [2, 3, 4, 4, 5, 6, 7, 8]
    })

    st.dataframe(data, use_container_width=True, hide_index=True)

    clusters = st.slider("Number of clusters", 2, 4, 2)

    model = KMeans(
        n_clusters=clusters,
        random_state=42,
        n_init=10
    )

    result = data.copy()
    result["Cluster"] = model.fit_predict(data)

    st.markdown("### Cluster results")

    st.dataframe(result, use_container_width=True, hide_index=True)

    st.caption(
        "Synthetic sample data only. This does not predict mental health."
    )


# ==================================================
# WEEKLY WELLNESS REPORT
# ==================================================

def report_page():

    st.markdown("## 📄 Weekly Wellness Report")

    if not st.session_state.assessments:

        st.info("Complete some assessments before creating a report.")
        return

    df = pd.DataFrame(st.session_state.assessments)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    cutoff = datetime.now() - timedelta(days=7)

    weekly = df[df["date"] >= cutoff]

    st.write(f"Assessments during the last seven days: {len(weekly)}")

    if not weekly.empty:

        st.bar_chart(
            weekly[["stress", "sleep", "energy", "focus"]]
        )

    if st.button("Prepare PDF report", type="primary"):

        try:

            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table
            )
            from reportlab.lib.styles import getSampleStyleSheet

            buffer = io.BytesIO()

            doc = SimpleDocTemplate(buffer, pagesize=A4)

            styles = getSampleStyleSheet()

            story = [
                Paragraph(
                    "MindCare AI - Weekly Wellness Report",
                    styles["Title"]
                ),
                Spacer(1, 16),
                Paragraph(
                    f"Generated: {datetime.now().strftime('%d %B %Y')}",
                    styles["Normal"]
                ),
                Spacer(1, 16),
                Paragraph(
                    f"Assessments: {len(weekly)}",
                    styles["Normal"]
                )
            ]

            if not weekly.empty:

                columns = [
                    "mood", "stress", "sleep", "energy", "focus"
                ]

                table_data = [columns]

                for _, row in weekly[columns].iterrows():

                    table_data.append([
                        str(row[column])
                        for column in columns
                    ])

                story.append(Spacer(1, 15))
                story.append(Table(table_data, repeatRows=1))

            story.append(Spacer(1, 15))

            story.append(
                Paragraph(
                    "Educational self-reflection report only. "
                    "Not a clinical assessment.",
                    styles["Normal"]
                )
            )

            doc.build(story)

            buffer.seek(0)

            st.download_button(
                "Download weekly PDF",
                data=buffer,
                file_name="MindCare_AI_Weekly_Report.pdf",
                mime="application/pdf"
            )

        except Exception:
            st.error("PDF generation failed. Check the report dependencies.")


# ==================================================
# CRISIS SUPPORT
# ==================================================

def crisis_page():

    st.markdown("## 🆘 Crisis Support")

    st.error(
        "If you or another person is in immediate danger, contact emergency "
        "services or go to the nearest emergency department."
    )

    st.markdown("""
    ### 💚 You do not have to manage a difficult moment alone.

    - Contact a trusted family member, teacher, counsellor or responsible adult.
    - If you feel unsafe, move near a trusted person and ask them to stay with you.
    - For immediate emergency assistance in India, call **112**.
    - Reach out to a qualified professional for mental health support.

    MindCare AI is not an emergency response service.
    """)


# ==================================================
# SUPPORT RESOURCES
# ==================================================

def resources_page():

    st.markdown("## 📚 Support Resources")

    st.markdown("""
    ### 🇮🇳 Emergency support
    **112** – Emergency response in India

    [Official emergency response website](https://112.gov.in/)

    ---

    ### 💚 Tele-MANAS
    **14416** – Mental health support in India

    [Official Tele-MANAS website](https://telemanas.mohfw.gov.in/)

    ---

    ### 🌍 World Health Organization
    [Mental health information](https://www.who.int/health-topics/mental-health)
    """)


# ==================================================
# MAIN APPLICATION
# ==================================================

def main():

    t = LANG[st.session_state.language]

    if not st.session_state.logged_in:

        with st.sidebar:

            st.markdown("## 🌿 MindCare AI")

            st.selectbox(
                t["language"],
                list(LANG.keys()),
                key="language"
            )

        authentication_page(LANG[st.session_state.language])
        return

    with st.sidebar:

        st.markdown("## 🌿 MindCare AI")
        st.caption("Pause • Reflect • Recharge")

        st.selectbox(
            t["language"],
            list(LANG.keys()),
            key="language"
        )

        t = LANG[st.session_state.language]

        st.success(
            f"Welcome, {st.session_state.display_name}"
        )

        selected = st.radio(
            "Navigate",
            NAV,
            format_func=lambda key: t[key],
            index=NAV.index(st.session_state.page)
        )

        st.session_state.page = selected

        st.divider()

        if st.button(t["logout"], use_container_width=True):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.display_name = ""
            st.session_state.page = "home"

            st.rerun()

        st.caption("Neural Storm 2026")

    page = st.session_state.page

    if page == "home":
        home_page(t)

    elif page == "face":
        face_page()

    elif page == "assessment":
        assessment_page()

    elif page == "assistant":
        assistant_page()

    elif page == "mood":
        mood_page()

    elif page == "games":
        games_page()

    elif page == "stress":
        stress_page()

    elif page == "suggestions":
        suggestions_page()

    elif page == "voice":
        voice_page()

    elif page == "insights":
        insights_page()

    elif page == "playground":
        playground_page()

    elif page == "report":
        report_page()

    elif page == "crisis":
        crisis_page()

    elif page == "resources":
        resources_page()

    st.divider()

    st.caption(
        "🌿 MindCare AI | Neural Storm 2026 | Educational Wellbeing Support Prototype"
    )


main()

