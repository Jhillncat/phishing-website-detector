# Phishing Website Detector

## About

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

## How to Run

1. Clone this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt

3. Run the Streamlit app:

```bash
streamlit run app.py
