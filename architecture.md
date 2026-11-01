MindCare AI – System Architecture

1. Project Overview

MindCare AI is an educational wellbeing support application developed using Python, Streamlit, and Machine Learning concepts.

It provides interactive wellbeing activities, mood tracking, basic support conversations, visual insights, and educational machine learning demonstrations.

The application is designed as a learning prototype and is not a medical or diagnostic tool.

2. Technology Stack

Technology| Purpose
Python| Core application development
Streamlit| Web application interface
Pandas| Data handling and analysis
NumPy| Numerical operations
Scikit-learn| Machine Learning demonstration
MediaPipe| Facial landmark visualization
Pillow| Image processing
ReportLab| PDF report generation
Matplotlib / Streamlit charts| Data visualization

3. System Modules

3.1 User Interface Module

- Welcome page and dashboard
- Sidebar navigation
- Interactive buttons and forms
- Multilingual interface options

3.2 Face Expression Studio

- Captures an image using the camera input.
- Uses MediaPipe to identify facial landmarks.
- Displays facial landmark points and connections.
- Shows basic visible facial-expression observations.

Limitation: Facial landmarks and visible expressions cannot reliably determine a person's actual emotions or mental health condition.

3.3 Wellbeing Assessment

- Collects user-selected wellbeing information.
- Records mood, stress, sleep, energy, and focus.
- Displays feedback based on user responses.

3.4 AI Support Assistant

- Provides basic rule-based support responses.
- Supports the languages implemented in the application.
- Offers general educational wellbeing guidance.

3.5 Daily Mood Tracker

- Allows users to record daily mood check-ins.
- Maintains records during the application session.
- Displays mood history.

3.6 Mindful Mini Games

- Includes simple interactive activities.
- Provides observation, memory, and gratitude exercises.
- Encourages short mindful breaks.

3.7 Stress Relief Assistant

- Provides guided breathing activities.
- Includes grounding exercises.
- Offers study-break and relaxation suggestions.

3.8 Personalised Recommendations

- Provides suggestions based on user-selected needs.
- Offers general study, sleep, relaxation, and wellbeing tips.

3.9 Voice Assistant

- Provides an audio recording interface.
- Supports typed messages as an alternative.

Limitation: Audio recording does not automatically provide speech-to-text transcription or spoken responses unless those capabilities are separately implemented.

3.10 Wellbeing Insights

- Displays recorded wellbeing information.
- Uses charts to visualize available session data.
- Helps users observe patterns in their check-ins.

3.11 Machine Learning Demonstration

- Uses synthetic wellbeing data.
- Demonstrates the K-Means clustering algorithm.
- Shows how user-selected numerical features can be grouped.

This is an educational ML demonstration, not a mental health prediction model.

3.12 Weekly Wellness Report

- Summarizes available wellbeing records.
- Displays charts and basic statistics.
- Generates a downloadable PDF report.

3.13 Crisis Support and Resources

- Displays supportive guidance and relevant resources.
- Encourages users to contact a trusted person or qualified professional.
- Provides emergency contact information where appropriate.

4. System Workflow

1. The user opens the MindCare AI application.
2. The user selects a feature from the navigation menu.
3. The application collects the required user input.
4. Python processes the input according to the selected module.
5. The application displays feedback, activities, charts, or reports.
6. Relevant information is maintained in Streamlit session state.

5. Machine Learning Workflow

The educational ML demonstration follows these steps:

1. Generate or load synthetic wellbeing data.
2. Select numerical features.
3. Preprocess the data.
4. Apply the K-Means clustering algorithm.
5. Display the resulting clusters.
6. Present a basic cluster summary.

6. Data Management

- Streamlit session state is used to maintain application data during a session.
- The current prototype does not use a permanent database.
- Session records may be lost when the session resets.
- Camera images should not be treated as permanent user records.

7. Application Architecture

                 USER
                   |
                   v
          STREAMLIT INTERFACE
                   |
          NAVIGATION MODULE
                   |
     +-------------+-------------+
     |             |             |
     v             v             v
  WELLBEING     SUPPORT       FACE LANDMARK
  FEATURES      FEATURES      VISUALIZATION
     |             |             |
     +-------------+-------------+
                   |
                   v
           PYTHON PROCESSING
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
   PANDAS /    SCIKIT-LEARN   MEDIAPIPE
    NUMPY       K-MEANS
       |           |           |
       +-----------+-----------+
                   |
                   v
          RESULTS AND INSIGHTS
                   |
          +--------+--------+
          |                 |
          v                 v
      CHARTS             PDF REPORT

8. Deployment

The application is designed to run using Streamlit.

Deployment platform: Streamlit Community Cloud

Dependencies are listed in "requirements.txt".

9. Project Limitations

- The application is an educational prototype.
- It does not diagnose or treat mental health conditions.
- Facial landmark observations are not reliable emotion measurements.
- The support assistant uses predefined responses rather than a trained conversational AI model.
- The current prototype does not provide permanent database storage.
- Voice recording does not itself guarantee speech recognition or speech generation.

10. Conclusion

MindCare AI demonstrates how Python, Streamlit, data analysis, computer vision, and Machine Learning concepts can be combined to develop an interactive educational wellbeing application.
