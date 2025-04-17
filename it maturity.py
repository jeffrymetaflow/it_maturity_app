import streamlit as st
import json
import pandas as pd

# Load grouped questions from JSON
with open("grouped_questions.json") as f:
    grouped_questions = json.load(f)

st.set_page_config(page_title="IT Maturity Assessment", layout="wide")
st.title("🧠 IT Maturity Assessment Tool")
st.markdown("""
Welcome to the interactive IT Maturity Assessment. Please answer the following questions 
based on your current IT environment. Your responses will be used to calculate a maturity score
across several technology domains.
""")

responses = {}
st.sidebar.header("Navigation")

# Questionnaire Form
with st.form("maturity_form"):
    for category, questions in grouped_questions.items():
        st.subheader(category.strip())
        for q in questions:
            key = f"{category.strip()}::{q}"
            responses[key] = st.radio(q.strip(), ["Yes", "No"], key=key)
    submitted = st.form_submit_button("Submit Assessment")

# Scoring and Results
if submitted:
    st.header("📊 Maturity Assessment Results")
    score_data = []

    for category in grouped_questions:
        questions = grouped_questions[category]
        yes_count = sum(
            1 for q in questions if responses.get(f"{category.strip()}::{q}") == "Yes"
        )
        total = len(questions)
        percent = round((yes_count / total) * 100, 1)
        score_data.append({"Category": category.strip(), "Score (%)": percent})

    score_df = pd.DataFrame(score_data).sort_values(by="Category")
    st.dataframe(score_df, use_container_width=True)

    st.bar_chart(score_df.set_index("Category"))

    st.markdown("""
    ### 🔍 Interpretation:
    - **80%+**: High maturity — optimized or automated
    - **50-79%**: Moderate maturity — standardized or in transition
    - **Below 50%**: Low maturity — ad-hoc or siloed
    """)
