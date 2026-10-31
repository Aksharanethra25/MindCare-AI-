🏗️ MindCare AI – System Architecture

1. Introduction

MindCare AI is an educational mental wellbeing awareness application developed using Python and Streamlit.

The system combines interactive user input, predefined support responses, synthetic data processing, and machine learning demonstrations.

2. System Architecture

The application consists of four main modules:

Module 1: User Interface

- Developed using Streamlit.
- Provides navigation between application pages.
- Collects optional wellbeing reflections.

Module 2: Wellbeing Check-in

- Collects mood, energy, and sleep-related responses.
- Displays the current check-in information.
- Provides a simple reflection experience.

Module 3: Support Assistant

- Uses predefined keyword-based rules.
- Provides general wellbeing information.
- Encourages appropriate human support.

Module 4: Machine Learning

- Uses synthetic wellbeing data.
- Performs data preprocessing.
- Applies K-Means clustering.
- Displays illustrative sample patterns.

3. System Workflow

1. User opens the MindCare AI application.
2. User selects an application module.
3. The check-in module collects optional responses.
4. The support assistant provides predefined information.
5. The ML module processes synthetic sample data.
6. Visualisations display the resulting sample patterns.
7. The support resources page provides further guidance.

4. Technology Architecture

Layer| Technology
Frontend| Streamlit
Programming| Python
Data Processing| Pandas, NumPy
Machine Learning| Scikit-learn
Visualisation| Matplotlib
Development| Google Colab
Repository| GitHub
Deployment| Streamlit Community Cloud

5. Data Flow

The ML demonstration uses synthetic data rather than personal health records.

Synthetic Dataset → Data Preprocessing → Feature Scaling → K-Means Clustering → Sample Visualisation

6. Security and Privacy

- No permanent journal storage is intended in the current prototype.
- Synthetic data is used for ML experiments.
- No clinical diagnosis is generated.
- The application is not a substitute for professional care.

7. Conclusion

The modular architecture makes MindCare AI easier to understand, maintain, and extend. It demonstrates the integration of web development, data processing, and machine learning for responsible wellbeing awareness.
