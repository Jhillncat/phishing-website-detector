# Phishing Website Detector

## About
## Live Demo

Try the web app here:

https://phishing-website-detector-dtaykmafvcejv8ujiuxr8y.streamlit.app/

This project uses machine learning to classify websites as legitimate or phishing based on URL features.

The project uses the PhiUSIIL Phishing URL Dataset and a Random Forest classifier.

## Model

The final web app uses a Random Forest model with 100 trees.

The model was trained using an 80/20 stratified train-test split with `random_state=42`.

The web app uses 16 URL-based features:

- URLLength
- DomainLength
- IsDomainIP
- CharContinuationRate
- TLDLength
- NoOfSubDomain
- HasObfuscation
- NoOfObfuscatedChar
- ObfuscationRatio
- NoOfLettersInURL
- LetterRatioInURL
- NoOfEqualsInURL
- NoOfQMarkInURL
- NoOfAmpersandInURL
- NoOfOtherSpecialCharsInURL
- IsHTTPS

## Results

The final URL-based model achieved:

- Accuracy: 99.68%
- Precision: 99.83%
- Recall: 99.42%
- F1 Score: 99.63%

## How to Run

1. Clone this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt

3. Run the Streamlit app:

```bash
streamlit run app.py
