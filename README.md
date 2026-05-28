# Expert System: Gaming PC Builder Advisor
#### Done by: Shahmeer Shahzad | FA24-BCS-103

**Live Application:** [Click here to use the web app](https://ai-pc-builder-nq7xespnhacbpgwyi5n9wn.streamlit.app/)

## Project Overview
This project is a rule-based expert system designed to recommend optimal PC hardware configurations. It utilizes a custom-built, forward-chaining inference engine written in pure Python and features an interactive web interface powered by Streamlit.

The system evaluates user constraints (budget, resolution, workloads) against a knowledge base of over 50 hardware rules, resolving bottlenecks and architectural conflicts to produce a scientifically balanced system build alongside an explainable reasoning log.

---

## How to Run the Application

1. **Install Dependencies:**
   Ensure you have Python installed. Open your terminal in the project directory and run:
   ```bash
   pip install -r requirements.txt

2. **Launch the Expert System:**
   Start the Streamlit web server by running in the terminal:
   ```bash
   streamlit run app.py
