import streamlit as st
from review_modules import CodeAnalyzer, LLMReviewer, categorize_feedback, RuleBasedValidator, merge_reviews

# Optional: load OpenAI API key securely
import openai
openai.api_key = "This is secret." # Insert your API key here.

st.set_page_config(page_title="Code Review Assistant", layout="wide")
st.title("LLM-Powered Code Review System")

st.markdown("""
Upload a Python file or paste code below to receive GPT-based feedback and static rule validation.
""")

uploaded_file = st.file_uploader("Upload a .py file", type=["py"])
code_input = ""

if uploaded_file:
    code_input = uploaded_file.read().decode("utf-8")
else:
    code_input = st.text_area("Or paste your Python code below:", height=300)

if st.button("Run Code Review"):
    if not code_input.strip():
        st.warning("Please provide code to analyze.")
    else:
        with st.spinner("Analyzing with GPT..."):
            reviewer = LLMReviewer()
            result = reviewer.review_code(code_input)
            feedback = result["feedback"]
            categorized = categorize_feedback(feedback)

        with st.spinner("Running static rule-based validation..."):
            validator = RuleBasedValidator(code_input)
            static = validator.run_all_checks()
            combined = merge_reviews(categorized, static)

        with st.expander("LLM Raw Feedback", expanded=True):
            cleaned = feedback.replace("###", "####").strip()
            st.markdown(cleaned)

            st.download_button(
                label="Download Feedback as .txt",
                data=cleaned,
                file_name="code_review.txt",
                mime="text/plain"
    )
        import html

        st.subheader("Categorized Issues")

        category_colors = {
            "Security": "red",
            "Documentation": "blue",
            "Style": "green",
            "Bug": "orange"
        }
        for category, issues in combined.items():
            color = category_colors.get(category, "gray")
            st.markdown(f"<h4 style='color:{color};'>{category} ({len(issues)})</h4>", unsafe_allow_html=True)
            for i, issue in enumerate(issues, 1):
                clean = html.escape(issue.replace("####", "").strip())
                st.markdown(f"- {clean}")
            st.markdown("<hr>", unsafe_allow_html=True)



