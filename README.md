# Phishing Website Detector

## About
This project uses machine learning to classify websites as legitimate or phishing based on URL features.

The project uses the PhiUSIIL Phishing URL Dataset and a Random Forest classifier.

## Live Demo

Try the web app here:

https://phishing-website-detector-dtaykmafvcejv8ujiuxr8y.streamlit.app/

This project uses machine learning to classify websites as legitimate or phishing based on URL features.

The project uses the PhiUSIIL Phishing URL Dataset and a Random Forest classifier.

## Model

The final web app uses a Random Forest model with 100 trees.

The model was trained using an 80/20 stratified train-test split with `random_state=42`.

The web app uses 11 URL-based features:

- DomainLength
- IsDomainIP
- TLDLength
- NoOfSubDomain
- HasObfuscation
- NoOfObfuscatedChar
- ObfuscationRatio
- NoOfEqualsInURL
- NoOfQMarkInURL
- NoOfAmpersandInURL
- IsHTTPS

## Results

The final URL-based model achieved:

- Accuracy: 90.35%
- Precision: 95.61%
- Recall: 81.18%
- F1 Score: 87.86%

The model was evaluated on a held-out test set using the same 80/20 stratified split.

The confusion matrix was:

```text
[[16389, 3800],
 [  752, 26218]] 
```
## How to Run

1. Clone this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
```
3. Run the Streamlit app:

```bash
streamlit run app.py
```
## Project Notebook

The full model development and evaluation process was completed in Google Colab.

The complete project notebook is available on Google Colab:

https://colab.research.google.com/drive/1AWhiEou4WDQnDvjZeiXd_x-D9PElNKHL?usp=sharing

The notebook contains the data preprocessing, model training, evaluation, feature analysis, and experiments used for the project.
## AI Assistance

AI tools were used to help with testing the web app, troubleshooting issues, and learning how to connect and use Google Colab, GitHub, and Streamlit together. Since Streamlit was new to the student, AI assistance was also used to troubleshoot the cross-platform setup and deployment process.

All final code, model results, analysis, and project decisions were written, reviewed, and tested by the student.

## Disclaimer

This application is a research prototype. Predictions should not be treated as a guarantee that a website is safe or malicious.
