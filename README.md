# LLM-Powered Automated Code Review System

This project introduces a hybrid code review system that integrates the contextual reasoning capabilities of large language models (LLMs) with the reliability of rule-based static analysis. Built with Streamlit, the application offers developers automated, categorized, and interpretable feedback on Python code, supporting multiple dimensions of software quality such as style, documentation, logic, modularity, and security.

## Features

- LLM-powered review using OpenAI GPT-3.5
- Rule-based static validation using AST traversal and regex
- Categorized feedback: Style, Bug, Security, Documentation, Modularity
- Interactive Streamlit interface for file upload or code input
- Downloadable plaintext reports
- Session history and structured prompt logging

## System Overview

1. **Code Parsing and Feature Extraction**  
   The system uses Python’s AST module to extract structural metrics including function length, cyclomatic complexity, and duplication.

2. **Static Validation Module**  
   Custom rules detect insecure patterns, missing type hints, unused imports, and hardcoded secrets.

3. **LLM Review Engine**  
   Code is submitted to GPT-3.5 with a structured prompt, requesting feedback on correctness, readability, security, and documentation.

4. **Feedback Categorization**  
   The output from the LLM is processed using pattern matching and keyword-based classification.

5. **Streamlit Front-End**  
   Results are grouped by category and displayed in collapsible sections. Reports can be exported in plaintext format.

## File Structure

| File                      | Description                                      |
|---------------------------|--------------------------------------------------|
| `app.py`                  | Main Streamlit interface logic                   |
| `review_modules.py`       | Static validation, categorization, and parsing   |
| `example_*.py`            | Sample code files used for testing               |
| `test.py`                 | Simple test script for validation                |
| `LLM Project.ipynb`       | Development notebook and testing logs            |
| `README.md`               | Project documentation                            |

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Wendy-Ju/LLM-Powered-Automated-Code-Review-System.git
cd LLM-Powered-Automated-Code-Review-System
pip install -r requirements.txt
```bash

## Set your OpenAI API key as an environment variable:
export OPENAI_API_KEY=your_key_here
## Run the application:
streamlit run app.py

