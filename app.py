
import streamlit as st
import pandas as pd
import joblib
import re
import ipaddress
from urllib.parse import urlparse

# load model
model = joblib.load("phishing_app_model.pkl")
app_features = joblib.load("app_features.pkl")


# get features from the url
def extract_app_features(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc.split("@")[-1].split(":")[0]

    domain_length = len(domain)

    try:
        ipaddress.ip_address(domain)
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0

    domain_parts = domain.split(".")
    tld = domain_parts[-1] if len(domain_parts) > 1 else ""

    tld_length = len(tld)
    no_of_subdomain = max(len(domain_parts) - 2, 0)

    obfuscated_matches = re.findall(r"%[0-9A-Fa-f]{2}", url)
    no_of_obfuscated_char = len(obfuscated_matches)

    has_obfuscation = (
        1 if no_of_obfuscated_char > 0 or "@" in url else 0
    )

    obfuscation_ratio = (
        no_of_obfuscated_char / len(url) if len(url) > 0 else 0
    )

    no_of_equals = url.count("=")
    no_of_qmark = url.count("?")
    no_of_ampersand = url.count("&")

    is_https = 1 if parsed.scheme == "https" else 0

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


# clear the url
def clear_url():
    st.session_state.url_input = ""


st.set_page_config(
    page_title="Phishing Website Detector",
    layout="centered"
)

st.title("Phishing Website Detector")

st.write(
    "Enter a website URL below to analyze its phishing risk "
    "using a machine learning model."
)

st.info(
    "This application uses a Random Forest classifier trained "
    "on URL-based features from the PhiUSIIL phishing URL dataset."
)


# explain how to use the app
with st.expander("How to use this app"):
    st.write("1. Enter a website URL.")
    st.write("2. Click **Analyze Website**.")
    st.write("3. Review the prediction, phishing probability, and risk level.")
    st.write(
        "4. To test another URL, replace the current URL and click "
        "**Analyze Website** again."
    )
    st.write(
        "5. You can also use **Clear URL** to remove the current URL."
    )


url = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com",
    key="url_input"
)


col1, col2 = st.columns(2)

with col1:
    analyze_button = st.button(
        "Analyze Website",
        type="primary",
        use_container_width=True
    )

with col2:
    st.button(
        "Clear URL",
        on_click=clear_url,
        use_container_width=True
    )


# analyze the current url
if analyze_button:
    if not url.strip():
        st.warning("Please enter a website URL.")
    else:
        try:
            # get features from the current url
            features = extract_app_features(url)

            input_data = pd.DataFrame([features])
            input_data = input_data[app_features]

            # run a new prediction each time the button is pressed
            prediction = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]

            phishing_index = list(model.classes_).index(0)
            phishing_probability = probabilities[phishing_index]

            st.subheader("Analysis Result")

            if prediction == 0:
                st.error("PHISHING WEBSITE DETECTED")
            else:
                st.success("WEBSITE CLASSIFIED AS LEGITIMATE")

            st.metric(
                "Model-Estimated Phishing Probability",
                f"{phishing_probability * 100:.2f}%"
            )


            # risk level
            if phishing_probability >= 0.70:
                st.error("Risk Level: HIGH")
            elif phishing_probability >= 0.40:
                st.warning("Risk Level: MEDIUM")
            else:
                st.success("Risk Level: LOW")


            # explain the result
            st.subheader("How to Interpret This Result")

            st.write(
                f"The model estimated a **{phishing_probability * 100:.2f}%** "
                "probability that this URL belongs to the phishing class."
            )

            st.write(
                "**Risk levels:** Low = below 40%, "
                "Medium = 40% to below 70%, "
                "High = 70% or higher."
            )

            st.caption(
                "The phishing probability is a model estimate and is not "
                "a guarantee that a website is safe or malicious."
            )


            # explain the url features
            with st.expander("What do the URL features mean?"):
                st.write(
                    "The model uses characteristics that can be calculated "
                    "directly from the submitted URL."
                )

                st.write(
                    "- **Length features:** measure the length of parts of the URL."
                )

                st.write(
                    "- **Count features:** count characters, subdomains, "
                    "or other URL elements."
                )

                st.write(
                    "- **Binary features:** use 0 or 1 to indicate whether "
                    "a characteristic is present."
                )

                st.write(
                    "- **Obfuscation ratio:** represents the proportion of "
                    "the URL associated with encoded characters."
                )

                st.write(
                    "The exact numerical range depends on the feature. "
                    "For example, binary features use 0 or 1, count features "
                    "are non-negative values, and the obfuscation ratio is "
                    "between 0 and 1."
                )


            # show feature values
            with st.expander("View URL Features Analyzed"):
                feature_display = pd.DataFrame({
                    "Feature": input_data.columns,
                    "Value": input_data.iloc[0].values
                })

                st.dataframe(
                    feature_display,
                    use_container_width=True,
                    hide_index=True
                )


            st.info(
                "To analyze another website, replace the URL above and "
                "click **Analyze Website** again, or click **Clear URL**."
            )

        except Exception as e:
            st.error(f"Unable to analyze this URL: {e}")


st.caption(
    "This application is a research prototype. Its prediction should not "
    "be treated as a guarantee that a website is safe or malicious."
)

