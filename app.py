import streamlit as st
import pandas as pd
import numpy as np
import random
import io
import os
from datetime import datetime, date, timedelta
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw

# Optional face landmark support
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except Exception:
    mp = None
    MEDIAPIPE_AVAILABLE = False

# Optional voice output
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except Exception:
    GTTS_AVAILABLE = False

# Supabase connection
try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except Exception:
    SUPABASE_AVAILABLE = False


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# BEAUTIFUL DESIGN
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #f4fbf8 50%, #fff5f8 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(120deg, #102f42, #087f72, #36b99b);
    color: white;
    padding: 42px 38px;
    border-radius: 28px;
    margin-bottom: 22px;
    box-shadow: 0 12px 35px rgba(15, 90, 85, 0.16);
}

.hero h1 {
    color: white;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #e4fff6;
    font-size: 17px;
}

.section-card {
    background: rgba(255,255,255,0.88);
    padding: 23px;
    border: 1px solid #e6eee9;
    border-radius: 20px;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(30,70,60,0.05);
}

.feature-card {
    background: white;
    border: 1px solid #e7eee9;
    border-radius: 20px;
    padding: 20px;
    min-height: 145px;
    box-shadow: 0 5px 18px rgba(30,70,60,0.05);
}

.feature-card h3 {
    color: #14594e;
    font-size: 19px;
}

.small-muted {
    color: #71817d;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 13px;
    border: 0;
    font-weight: 700;
    min-height: 42px;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #087f72, #32b995);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e9f7f1, #f1f1ff);
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: #174f49;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MULTILINGUAL TEXT
# --------------------------------------------------

LANGUAGES = {
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
        "register": "Create account",
        "login": "Login",
        "logout": "Logout",
        "save": "Save",
        "submit": "Submit",
        "mood_question": "How are you feeling today?",
        "privacy": "Your information should be kept private and secure.",
        "login_required": "Please create an account or log in to continue.",
        "not_configured": "Account services are not configured yet. Please add your Supabase credentials."
    },
    "தமிழ்": {
        "welcome": "MindCare AI-க்கு வரவேற்கிறோம்",
        "tagline": "உங்கள் மனநலத்தைப் பற்றி சிந்திக்கவும், ஊக்கம் பெறவும் உதவும் இடம்.",
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
        "report": "வாராந்திர நலவாழ்வு அறிக்கை",
        "crisis": "அவசர ஆதரவு",
        "resources": "ஆதரவு வளங்கள்",
        "language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "name": "உங்கள் பெயர்",
        "email": "மின்னஞ்சல் முகவரி",
        "username": "பயனர் பெயர்",
        "password": "கடவுச்சொல்",
        "register": "கணக்கை உருவாக்கு",
        "login": "உள்நுழை",
        "logout": "வெளியேறு",
        "save": "சேமி",
        "submit": "சமர்ப்பி",
        "mood_question": "இன்று நீங்கள் எப்படி உணர்கிறீர்கள்?",
        "privacy": "உங்கள் தகவல்கள் பாதுகாப்பாக வைக்கப்பட வேண்டும்.",
        "login_required": "தொடர கணக்கை உருவாக்கவும் அல்லது உள்நுழையவும்.",
        "not_configured": "கணக்கு சேவை இன்னும் அமைக்கப்படவில்லை. Supabase விவரங்களைச் சேர்க்கவும்."
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
        "register": "അക്കൗണ്ട് സൃഷ്ടിക്കുക",
        "login": "ലോഗിൻ",
        "logout": "ലോഗ്ഔട്ട്",
        "save": "സേവ്",
        "submit": "സമർപ്പിക്കുക",
        "mood_question": "ഇന്ന് നിങ്ങൾക്ക് എങ്ങനെ തോന്നുന്നു?",
        "privacy": "നിങ്ങളുടെ വിവരങ്ങൾ സുരക്ഷിതമായി സൂക്ഷിക്കണം.",
        "login_required": "തുടരാൻ അക്കൗണ്ട് സൃഷ്ടിക്കുകയോ ലോഗിൻ ചെയ്യുകയോ ചെയ്യുക.",
        "not_configured": "Supabase ക്രമീകരണം ആവശ്യമാണ്."
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
        "register": "ఖాతా సృష్టించండి",
        "login": "లాగిన్",
        "logout": "లాగ్అవుట్",
        "save": "సేవ్",
        "submit": "సమర్పించండి",
        "mood_question": "ఈ రోజు మీకు ఎలా అనిపిస్తోంది?",
        "privacy": "మీ సమాచారం సురక్షితంగా ఉండాలి.",
        "login_required": "కొనసాగడానికి ఖాతా సృష్టించండి లేదా లాగిన్ అవ్వండి.",
        "not_configured": "Supabase సెట్టింగ్ అవసరం."
    },
    "हिन्दी": {
        "welcome": "MindCare AI में आपका स्वागत है",
        "tagline": "आपके रोज़मर्रा के स्वास्थ्य और आत्मचिंतन के लिए एक मित्रवत स्थान।",
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
        "register": "खाता बनाएँ",
        "login": "लॉगिन",
        "logout": "लॉगआउट",
        "save": "सेव करें",
        "submit": "जमा करें",
        "mood_question": "आज आप कैसा महसूस कर रहे हैं?",
        "privacy": "आपकी जानकारी सुरक्षित रखी जानी चाहिए।",
        "login_required": "आगे बढ़ने के लिए खाता बनाएँ या लॉगिन करें।",
        "not_configured": "Supabase सेटअप आवश्यक है।"
    }
}

NAV_KEYS = [
    "home", "face", "assessment", "assistant", "mood", "games",
    "stress", "suggestions", "voice", "insights", "playground",
    "report", "crisis", "resources"
]


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "user": None,
    "profile": None,
    "language": "English",
    "page": "home",
    "chat_messages": [],
    "last_assessment": None,
    "game_points": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# SUPABASE CLIENT
# --------------------------------------------------

def get_supabase():
    if not SUPABASE_AVAILABLE:
        return None

    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        return create_client(url, key)
    except Exception:
        return None


supabase = get_supabase()


def save_record(table, record):
    if supabase is None or st.session_state.user is None:
        return False

    try:
        record["user_id"] = st.session_state.user.id
        supabase.table(table).insert(record).execute()
        return True
    except Exception as error:
        st.error("Could not save your record. Please check your database setup.")
        return False


def load_records(table, limit=100):
    if supabase is None or st.session_state.user is None:
        return []

    try:
        response = (
            supabase.table(table)
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []
    except Exception:
        return []


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

def auth_page():
    t = LANGUAGES[st.session_state.language]

    st.markdown("""
    <div class="hero">
        <h1>🌿 MindCare AI</h1>
        <p>Your personal space for reflection, encouragement and everyday wellbeing.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ Create your personal MindCare space")
    st.write("Create an account to keep your wellbeing records private to your account.")

    if supabase is None:
        st.error(t["not_configured"])
        st.info(
            "Before account registration can work, create a Supabase project "
            "and add SUPABASE_URL and SUPABASE_ANON_KEY to Streamlit secrets."
        )
        st.code(
            '[supabase]\\n'
            'SUPABASE_URL = "https://YOUR-PROJECT.supabase.co"\\n'
            'SUPABASE_ANON_KEY = "YOUR-ANON-KEY"',
            language="toml"
        )
        return

    mode = st.radio(
        "Choose an option",
        ["Create Account", "Login"],
        horizontal=True
    )

    if mode == "Create Account":
        with st.form("register_form"):
            name = st.text_input(t["name"])
            email = st.text_input(t["email"])
            username = st.text_input(t["username"])
            password = st.text_input(t["password"], type="password")
            confirm = st.text_input("Confirm password", type="password")
            accepted = st.checkbox(
                "I understand this is an educational wellbeing application."
            )
            submitted = st.form_submit_button(
                t["register"], type="primary", use_container_width=True
            )

            if submitted:
                if not all([name, email, username, password, confirm]):
                    st.warning("Please complete all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 8:
                    st.error("Use a password with at least 8 characters.")
                elif not accepted:
                    st.warning("Please confirm the educational-use notice.")
                else:
                    try:
                        result = supabase.auth.sign_up({
                            "email": email.strip(),
                            "password": password,
                            "options": {
                                "data": {
                                    "name": name.strip(),
                                    "username": username.strip()
                                }
                            }
                        })

                        if result.user:
                            st.success(
                                "Account created. If email confirmation is enabled, "
                                "check your inbox and confirm your email before logging in."
                            )
                        else:
                            st.info("Please check your email for the confirmation link.")
                    except Exception:
                        st.error(
                            "Account creation failed. Check whether this email is "
                            "already registered and review Supabase settings."
                        )

    else:
        with st.form("login_form"):
            email = st.text_input(t["email"])
            password = st.text_input(t["password"], type="password")
            submitted = st.form_submit_button(
                t["login"], type="primary", use_container_width=True
            )

            if submitted:
                try:
                    result = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password
                    })

                    if result.user:
                        st.session_state.user = result.user
                        st.session_state.profile = result.user.user_metadata or {}
                        st.session_state.page = "home"
                        st.rerun()
                except Exception:
                    st.error("Login failed. Check your email and password.")


# --------------------------------------------------
# WELCOME PAGE
# --------------------------------------------------

def welcome_page(t):
    profile = st.session_state.profile or {}
    display_name = profile.get("name", "Friend")

    st.markdown(f"""
    <div class="hero">
        <h1>🌿 {t['welcome']}</h1>
        <p>{t['tagline']}</p>
        <p>Pause • Reflect • Recharge ✨</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"## 👋 Welcome, {display_name}!")

    st.markdown("""
    <div class="section-card">
        <h2>💚 What is MindCare AI?</h2>
        <p>
        MindCare AI is an educational wellbeing companion designed to help
        you reflect on your day, understand your own wellbeing patterns,
        explore mindful activities and discover supportive resources.
        </p>
        <p>
        It is not a medical service, diagnostic tool or replacement for
        professional care.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✨ Explore your wellbeing toolkit")

    cards = [
        ("😊", t["face"], "Explore facial landmarks and visible features."),
        ("🌿", t["assessment"], "Reflect on sleep, energy, focus and stress."),
        ("🤖", t["assistant"], "Chat with a supportive educational assistant."),
        ("📅", t["mood"], "Record your daily mood check-ins."),
        ("🎮", t["games"], "Try gentle mindful mini-games."),
        ("🧘", t["stress"], "Explore calming activities and grounding."),
        ("✨", t["suggestions"], "Explore helpful everyday suggestions."),
        ("🎙️", t["voice"], "Use audio recording and spoken responses."),
        ("📊", t["insights"], "View your recorded wellbeing patterns."),
        ("🧪", t["playground"], "Explore a simple machine-learning demo."),
        ("📄", t["report"], "Create a report from your saved records."),
        ("🆘", t["crisis"], "Find support when you need it."),
        ("📚", t["resources"], "Explore trusted support resources.")
    ]

    cols = st.columns(3)
    for index, item in enumerate(cards):
        with cols[index % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <h2>{item[0]}</h2>
                <h3>{item[1]}</h3>
                <p class="small-muted">{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.info("Choose a section from the sidebar to get started.")


# --------------------------------------------------
# FACE EXPRESSION STUDIO
# --------------------------------------------------

def face_page(t):
    st.markdown("## 😊 Face Expression Studio")
    st.write(
        "Capture a selfie to explore facial landmarks. Facial appearance "
        "cannot reliably reveal someone's actual feelings or mental health."
    )

    photo = st.camera_input("Take your selfie")

    if photo:
        image = Image.open(photo).convert("RGB")
        st.image(image, caption="Your camera image", use_container_width=True)

        if not MEDIAPIPE_AVAILABLE:
            st.warning(
                "Facial landmark support is unavailable in this deployment. "
                "Other MindCare features remain available."
            )
        else:
            try:
                face_mesh = mp.solutions.face_mesh
                drawing = mp.solutions.drawing_utils
                styles = mp.solutions.drawing_styles

                with face_mesh.FaceMesh(
                    static_image_mode=True,
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5
                ) as mesh:
                    results = mesh.process(np.array(image))

                if results.multi_face_landmarks:
                    annotated = image.copy()
                    draw = ImageDraw.Draw(annotated)
                    width, height = annotated.size

                    for face in results.multi_face_landmarks:
                        points = []
                        for landmark in face.landmark:
                            x = int(landmark.x * width)
                            y = int(landmark.y * height)
                            points.append((x, y))

                        for x, y in points:
                            draw.ellipse(



