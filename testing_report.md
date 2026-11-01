🧪 MindCare AI – Testing Report

Application Testing and Quality Assessment

Domain: Python and Machine Learning (Python & ML)
Framework: Streamlit
Testing Document: Updated Application Version

---

1. Introduction

This document describes the testing plan for the updated MindCare AI educational wellbeing application.

The application is developed using Python and Streamlit and includes interactive wellbeing features, a basic machine-learning demonstration, multilingual navigation and support resources.

Testing is intended to verify application navigation, user interactions, feature availability and error handling.

2. Testing Objectives

- Verify that the Welcome Homepage appears first.
- Check the application navigation order.
- Verify language selection.
- Test demo registration and login.
- Check the facial landmark demonstration.
- Test wellbeing assessment and mood recording.
- Check chatbot responses.
- Test mindful games and stress-relief activities.
- Verify voice assistant behaviour.
- Check charts and PDF report generation.
- Test the K-Means demonstration.
- Verify crisis support and resource information.

3. Testing Environment

Component| Environment
Programming Language| Python
Web Framework| Streamlit
Data Processing| Pandas, NumPy
Machine Learning| Scikit-learn
Image Processing| Pillow
Facial Landmarks| MediaPipe (optional)
PDF Generation| ReportLab
Text-to-Speech| gTTS (optional)
Deployment| Streamlit Community Cloud
Repository| GitHub

4. Functional Test Cases

Test ID| Test Scenario| Expected Result| Status
TC01| Open application| Welcome page appears first| Pending
TC02| Select language| Selected language is applied to supported interface text| Pending
TC03| Create demo account| Account is created for the current session| Pending
TC04| Login with valid demo details| User enters the application| Pending
TC05| Navigate between modules| Correct module is displayed| Pending
TC06| Open Face Expression Studio| Camera input is available when supported| Pending
TC07| Capture a selfie| Facial landmarks are displayed when MediaPipe works| Pending
TC08| Submit wellbeing assessment| Assessment is recorded in session state| Pending
TC09| Send chatbot message| Rule-based response is displayed| Pending
TC10| Save mood check-in| Mood entry is recorded in the current session| Pending
TC11| Open mindful mini-games| Selected activity is displayed| Pending
TC12| Open Stress Relief Studio| Selected activity is displayed| Pending
TC13| View personalised suggestions| Relevant general suggestions are displayed| Pending
TC14| Record voice message| Audio recording is available when browser support exists| Pending
TC15| View wellbeing insights| Assessment charts are displayed when data exists| Pending
TC16| Run K-Means demonstration| Cluster assignments are displayed| Pending
TC17| Generate weekly report| PDF report is generated when data exists| Pending
TC18| Open Crisis Support| Emergency guidance is displayed| Pending
TC19| Open Support Resources| Resource information and links are displayed| Pending
TC20| Refresh or restart application| Temporary session-data behaviour is understood| Pending

5. Machine Learning Testing

The Python and ML Playground uses the K-Means clustering algorithm with synthetic educational data.

The following aspects should be checked:

- Sample data generation.
- Selection of the number of clusters.
- Successful K-Means execution.
- Display of cluster assignments.
- Correct handling of sample data.

The clustering demonstration is educational and does not diagnose or predict mental health conditions.

6. Error Handling and Compatibility Testing

The following conditions should be checked:

- Missing optional MediaPipe dependency.
- Camera permission unavailable.
- Empty user input.
- Missing assessment records.
- PDF generation errors.
- Browser audio limitations.
- Package installation and deployment errors.

The application should display an appropriate message instead of failing unnecessarily.

7. Testing Status

Current status: Testing in progress.

Test cases are listed for the updated application. Their results must be recorded only after the corresponding feature has been tested.

Testing Area| Status
Application startup| Pending verification
Welcome Homepage| Pending verification
Navigation| Pending verification
Language selection| Pending verification
Demo registration and login| Pending verification
Wellbeing modules| Pending verification
Face landmark demonstration| Pending verification
Voice features| Pending verification
Charts and PDF report| Pending verification
Machine-learning demonstration| Pending verification
Crisis support and resources| Pending verification

8. Known Limitations

- Demo accounts are stored only in Streamlit session state.
- Permanent user authentication is not configured.
- User records are not permanently stored in a database.
- The chatbot uses predefined rules.
- Automatic speech transcription is not implemented.
- Facial landmarks do not reveal actual emotions.
- Some detailed translations remain incomplete.
- The ML demonstration uses synthetic data.
- Clinical effectiveness has not been evaluated.

9. Conclusion

This testing report provides a structured plan for evaluating the updated MindCare AI application.

Further functional, compatibility and deployment testing is required before all modules can be marked as verified.

MindCare AI – Pause. Reflect. Recharge. 🌿
