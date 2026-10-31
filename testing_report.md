🧪 MindCare AI – Testing Report

1. Introduction

This document describes the functional testing performed on the MindCare AI educational prototype.

2. Testing Objectives

- Verify application navigation.
- Check wellbeing check-in functionality.
- Verify support assistant responses.
- Test synthetic dataset processing.
- Check machine learning demonstration output.
- Verify support resources display correctly.

3. Functional Test Cases

Test ID| Test Scenario| Expected Result
TC01| Open the application| Homepage loads
TC02| Navigate between pages| Correct page appears
TC03| Submit wellbeing check-in| Responses are displayed
TC04| Enter a supported keyword| Predefined response appears
TC05| Load synthetic dataset| Sample data loads
TC06| Run K-Means demonstration| Cluster assignments are generated
TC07| View data visualisation| Charts display correctly
TC08| Open support resources| Resource information appears

4. Testing Status

The application modules have been manually checked during development.

Module| Status
Homepage| Verified
Wellbeing Check-in| Verified
Support Assistant| Verified
ML Demonstration| Verified
Support Resources| Verified

5. Testing Environment

- Programming Language: Python
- Framework: Streamlit
- ML Library: Scikit-learn
- Data Processing: Pandas and NumPy
- Deployment: Streamlit Community Cloud

6. Limitations

- Testing is limited to the educational prototype.
- Synthetic data is used for ML demonstrations.
- Clinical effectiveness has not been evaluated.
- No clinical screening or crisis-detection validation has been performed.

7. Conclusion

The manual functional checks indicate that the main application modules operate as intended in the tested environment. Further testing is required before any real-world or clinical use.
