# Phishing Website Detector

## About
This project uses machine learning to classify websites as legitimate or phishing based on URL features.

The project uses the PhiUSIIL Phishing URL Dataset and a Random Forest classifier.

## Live Demo

Try the web app here:

https://phishing-website-detector-dtaykmafvcejv8ujiuxr8y.streamlit.app/

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

## Understanding the Results

### Phishing Probability
The phishing probability is the Random Forest model's estimated probability
that the submitted URL belongs to the phishing class. It ranges from 0% to 100%.

### Risk Level
- **Low:** phishing probability below 40%
- **Medium:** phishing probability from 40% to below 70%
- **High:** phishing probability of 70% or higher

### Model Prediction
The app classifies the submitted URL as either:
- **Legitimate**
- **Phishing**

These predictions and probabilities are model estimates and should not be
treated as a guarantee that a website is safe or malicious.

### Model Evaluation Metrics

- **Accuracy:** percentage of all test examples classified correctly.
- **Precision:** percentage of URLs predicted as phishing that were actually phishing.
- **Recall:** percentage of actual phishing URLs that the model successfully detected.
- **F1-score:** combines precision and recall into one metric.

For this project, recall is especially important because a false negative means
a phishing website was incorrectly classified as legitimate.

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

## How to Analyze Another URL

1. Enter a website URL in the input box.
2. Click **Analyze Website**.
3. Review the prediction, phishing probability, and risk level.
4. To test another website, click Clear URL or replace the current URL.
5. Enter the new URL and click Analyze Website again.
6. The app will run a new analysis using the new URL.
   
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
