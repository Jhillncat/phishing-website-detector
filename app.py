import streamlit as st
import pandas as pd
import joblib
import re
import ipaddress
from urllib.parse import urlparse


#load model
model = joblib.load("phishing_app_model.pkl")
app_features = joblib.load("app_features.pkl")


#get features from the url
def extract_app_features(url):

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc.split("@")[-1].split(":")[0]

    #domain length
    domain_length = len(domain)

    #check if domain is an ip
    try:
        ipaddress.ip_address(domain)
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0

    #get tld info
    domain_parts = domain.split(".")

    tld = domain_parts[-1] if len(domain_parts) > 1 else ""

    tld_length = len(tld)

    #count subdomains
    no_of_subdomain = max(len(domain_parts) - 2, 0)

    #check for obfuscation/complication
    obfuscated_matches = re.findall(
        r"%[0-9A-Fa-f]{2}",
        url
    )

    no_of_obfuscated_char = len(obfuscated_matches)
    has_obfuscation = (
        1
        if no_of_obfuscated_char > 0 or "@" in url
        else 0
    )
    obfuscation_ratio = (
        no_of_obfuscated_char / len(url)
        if len(url) > 0
        else 0
    )

    #count url characters
    no_of_equals = url.count("=")
    no_of_qmark = url.count("?")
    no_of_ampersand = url.count("&")

    #check if https
    is_https = (
        1
        if parsed.scheme == "https"
        else 0
    )
    return {
        "DomainLength": domain_length,
        "IsDomainIP": is_domain_ip,
        "TLDLength": tld_length,
        "NoOfSubDomain": no_of_subdomain,
        "HasObfuscation": has_obfuscation,
        "NoOfObfuscatedChar": no_of_obfuscated_char,
        "ObfuscationRatio": obfuscation_ratio,
        "NoOfEqualsInURL": no_of_equals,
        "NoOfQMarkInURL": no_of_qmark,
        "NoOfAmpersandInURL": no_of_ampersand,
        "IsHTTPS": is_https
    }

#page setup
st.set_page_config(
    page_title="Phishing Website Detector",
    layout="centered"
)

#page title
st.title(" Phishing Website Detector")
st.write(
    "Enter a website URL below to analyze its "
    "phishing risk using a machine learning model."
)

st.info(
    "This application uses a Random Forest classifier "
    "trained on URL-based features from the PhiUSIIL "
    "phishing URL dataset."
)

#url input
url = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com"
)

#analyze url
if st.button("Analyze Website", type="primary"):

    if not url.strip():
        st.warning("Please enter a website URL.")

    else:
        try:

            #get features / put into dataframe
            features = extract_app_features(url)
            input_data = pd.DataFrame(
                [features]
            )

            #keep features in the same order & make predics
            input_data = input_data[
                app_features
            ]
            prediction = model.predict(
                input_data
            )[0]

            #get prediction probabilities
            probabilities = model.predict_proba(
                input_data
            )[0]

            #get phishing probability
            phishing_index = list(
                model.classes_
            ).index(0)
            phishing_probability = (
                probabilities[phishing_index]
            )

            #show result
            st.subheader("Analysis Result")
            if prediction == 0:

                st.error(
                    "⚠️ PHISHING WEBSITE DETECTED"
                )

            else:

                st.success(
                    "WEBSITE CLASSIFIED AS LEGITIMATE"
                )

            #show probability
            st.metric(
                "Model-Estimated Phishing Probability",
                f"{phishing_probability * 100:.2f}%"
            )

            #set risk level
            if phishing_probability >= 0.70:
                st.error("Risk Level: HIGH")

            elif phishing_probability >= 0.40:

                st.warning("Risk Level: MEDIUM")

            else:
                st.success("Risk Level: LOW")

            #show features
            with st.expander(
                "View URL Features Analyzed"
            ):

                feature_display = pd.DataFrame({
                    "Feature": input_data.columns,
                    "Value": input_data.iloc[0].values
                })
                st.dataframe(
                    feature_display,
                    use_container_width=True,
                    hide_index=True
                )

            #disclaimers
            st.caption(
                "This application is a research prototype. "
                "Its prediction should not be treated as a "
                "guarantee that a website is safe or malicious."
            )

        except Exception as e:

            st.error(
                f"Unable to analyze this URL: {e}"
            )
