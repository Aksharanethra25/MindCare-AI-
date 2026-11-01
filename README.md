🌿 MindCare AI

An Educational Mental Wellbeing & Python and Machine Learning Support Platform

Hackathon: Neural Storm 2026
Track: Human Impact – HI-05
Domain: Python and Machine Learning (Python & ML)
Application: Streamlit Web Application

---

1. 📌 Project Overview

MindCare AI is an interactive educational wellbeing platform developed using Python, Streamlit and Machine Learning concepts.

It provides a friendly digital space where users can reflect on their daily wellbeing, record their moods, explore relaxation activities, interact with a supportive assistant and access useful support resources.

The application combines Python-based development, machine-learning demonstrations and interactive wellbeing features in one platform.

MindCare AI is an educational support prototype and is not a medical or diagnostic application.

2. 🎯 Problem Statement

Academic, social and personal responsibilities can affect everyday wellbeing. People may benefit from accessible digital tools that encourage self-reflection, positive habits and awareness of available support resources.

MindCare AI aims to provide an interactive platform for everyday wellbeing awareness and educational support.

3. 💡 Proposed Solution

MindCare AI brings multiple wellbeing activities together in one easy-to-use web application.

Users can:

- Explore facial landmarks through a camera-based demonstration.
- Complete personal wellbeing assessments.
- Record daily moods.
- Interact with a rule-based support assistant.
- Participate in mindful mini-games.
- Explore stress-relief activities.
- Receive general personalised suggestions.
- View wellbeing charts and reports.
- Explore basic machine-learning clustering.
- Access crisis and support resources.

4. 🎯 Project Objectives

1. Encourage everyday wellbeing awareness.
2. Provide simple self-reflection tools.
3. Promote mindful activities and positive habits.
4. Demonstrate Python programming and machine-learning concepts.
5. Provide multilingual navigation.
6. Make support information easier to access.
7. Develop an attractive and user-friendly web application.

5. ✨ Key Features

- 🌿 Beautiful Welcome Homepage
- 👤 Demo User Registration and Login
- 🌐 Five-language selection
- 😊 Face Expression Studio
- 📋 Wellbeing Assessment
- 🤖 AI Support Assistant
- 📅 Daily Mood Tracker
- 🎮 Mindful Mini Games
- 🧘 Stress Relief Studio
- ✨ Personalised Suggestions
- 🎙️ Voice Assistant
- 📊 Wellbeing Insights
- 🧪 Python and ML Playground
- 📄 Weekly Wellness Report
- 🆘 Crisis Support
- 📚 Support Resources

6. 🌐 Multilingual Support

The application provides language selection for:

1. English
2. Tamil
3. Malayalam
4. Telugu
5. Hindi

The current prototype translates the main navigation and selected interface prompts. Some detailed feature content and responses remain in English.

7. 🧩 Application Modules

7.1 Welcome Homepage

Introduces MindCare AI and provides access to the application's features.

7.2 Face Expression Studio

Allows users to capture a selfie and explore facial landmark points when the required MediaPipe package is available.

It does not determine actual emotions or diagnose mental health.

7.3 Wellbeing Assessment

Allows users to reflect on mood, stress, sleep, energy, focus and daily activity.

7.4 AI Support Assistant

Provides basic rule-based supportive responses to user messages.

7.5 Daily Mood Tracker

Allows users to record their daily mood and optional notes.

7.6 Mindful Mini Games

Includes colour check-in, gratitude activity, observation challenge and emoji memory activity.

7.7 Stress Relief Studio

Provides breathing pauses, grounding activities, study resets and positive reflection.

7.8 Personalised Suggestions

Provides general suggestions based on the user's selected area of interest.

7.9 Voice Assistant

Supports audio recording, typed messages and optional spoken responses. Automatic speech transcription is not included.

7.10 Wellbeing Insights

Displays charts based on wellbeing assessments recorded during the current application session.

7.11 Python and ML Playground

Demonstrates the K-Means clustering algorithm using synthetic educational data.

7.12 Weekly Wellness Report

Creates a PDF summary from available assessment records.

7.13 Crisis Support

Provides general guidance for reaching trusted people and emergency assistance.

7.14 Support Resources

Provides links to relevant wellbeing and emergency support resources.

8. 🧠 Machine Learning Demonstration

The Python and ML Playground demonstrates the K-Means clustering algorithm.

The demonstration:

- Uses synthetic sample data.
- Allows users to select the number of clusters.
- Displays the resulting cluster assignments.

This is an educational machine-learning demonstration and does not predict mental health conditions.

9. 📊 Dataset Description

The current application uses synthetic sample data for its K-Means demonstration.

User-entered mood and assessment information is maintained in Streamlit session state.

The current version does not have a connected permanent database.

10. 🔄 System Workflow

1. Open the MindCare AI web application.
2. Select a preferred language.
3. Create a temporary demo account or log in.
4. Enter the Welcome Homepage.
5. Select a feature from the navigation sidebar.
6. Complete assessments or activities.
7. View available charts and reports.
8. Access support resources when required.

11. 🛠️ Technologies Used

Technology| Purpose
Python| Application programming
Streamlit| Web application interface
Pandas| Data handling
NumPy| Numerical operations
Scikit-learn| K-Means clustering
MediaPipe| Optional facial landmark processing
Pillow| Image processing
ReportLab| PDF report generation
gTTS| Optional text-to-speech
GitHub| Source code management
Streamlit Community Cloud| Application deployment

12. 💻 System Requirements

- Python 3.11 or another compatible Python version.
- Internet connection.
- Modern web browser.
- Camera access for the selfie feature.
- Required Python packages listed in "requirements.txt".

13. ⚙️ Installation and Setup

Clone the repository:

git clone https://github.com/Aksharanethra25/MindCare-AI-.git

Move into the project directory:

cd MindCare-AI-

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

14. 🚀 How to Run the Application

1. Open the deployed MindCare AI website.
2. Select your preferred language.
3. Create a demo account.
4. Log in during the current session.
5. Explore the available application modules.
6. Try the wellbeing activities and machine-learning demonstration.

15. 📈 Results and Observations

The prototype brings multiple educational wellbeing features into a single Streamlit application.

It demonstrates:

- Interactive web application development using Python.
- Basic wellbeing self-reflection.
- Daily mood recording.
- Facial landmark visualisation when supported.
- Rule-based chatbot responses.
- K-Means clustering.
- Data visualisation.
- PDF report generation.

Actual performance and deployment results should be documented after testing.

16. 🌟 Advantages

- Simple and interactive interface.
- Multiple wellbeing features in one application.
- Five-language navigation.
- Educational machine-learning demonstration.
- Interactive mini-games.
- Accessible through a web browser.
- Support-resource information in one place.

17. ⚠️ Limitations

- Demo accounts are stored only in Streamlit session state.
- Passwords in the demo account implementation are not suitable for real authentication.
- User records are not permanently stored in a database.
- The chatbot uses rule-based responses, not a connected generative AI model.
- Automatic speech-to-text is not implemented.
- Voice recording and spoken output depend on browser and network support.
- Facial landmarks do not reveal a person's actual emotions.
- Detailed translations are not yet complete across every feature.
- Machine-learning data is synthetic.

18. 🔐 Privacy and Safety

MindCare AI is an educational wellbeing prototype.

- Do not enter sensitive personal information.
- Do not use real or reused passwords in demo accounts.
- Facial images are processed for the current demonstration and are not intentionally stored by the application.
- The application is not a replacement for qualified professional support.
- For immediate emergencies in India, contact 112.

19. 🔮 Future Enhancements

1. Secure authentication using Supabase.
2. Permanent user-specific database storage.
3. Complete translation of every feature into all five languages.
4. Advanced voice input and speech recognition.
5. Improved facial landmark visualisation.
6. More interactive mindful games.
7. Expanded Python and machine-learning demonstrations.
8. Improved personalised recommendations.
9. Enhanced PDF reporting.
10. More accessible and responsive interface design.

20. 🏁 Conclusion

MindCare AI demonstrates how Python programming and machine-learning concepts can be combined with Streamlit to create an interactive educational wellbeing platform.

By bringing self-reflection tools, mindful activities, visualisations and support resources together, the project aims to encourage everyday wellbeing awareness through an accessible digital experience.

MindCare AI – Pause. Reflect. Recharge. 🌿

---

🔗 Project Links

GitHub Repository:
https://github.com/Aksharanethra25/MindCare-AI-

Live Application:
https://aksharanethra25-mindcare-ai--app-mqe0vc.streamlit.app/

Hackathon: Neural Storm 2026
Domain: Python and Machine Learning (Python & ML)
