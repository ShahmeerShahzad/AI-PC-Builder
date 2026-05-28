import streamlit as st
from knowledge_base.engine import PCBuilderExpertSystem
from knowledge_base.rules import load_all_rules

# --- Page Config ---
st.set_page_config(page_title="AI PC Builder", page_icon="💻", layout="centered")
st.markdown("<h1 style='text-align: center; color: #00E5FF;'>💻 AI PC Builder Advisor</h1>", unsafe_allow_html=True)
st.write(
    "Configure your parameters below. The inference engine will evaluate the knowledge base, resolve hardware conflicts, and map out the required logic.")

# --- User Input Module ---
with st.form("pc_builder_form"):
    st.subheader("System Parameters")

    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Maximum Budget ($)", min_value=400, max_value=5000, value=850, step=50)
        resolution = st.selectbox("Target Resolution", ["1080p", "1440p", "4K"])
        preference = st.selectbox("CPU Brand Preference", ["No Preference", "AMD", "Intel"])
        form_factor = st.selectbox("Case Size", ["Standard Tower", "Small Form Factor (ITX)"])

    with col2:
        upgrade_path = st.selectbox("Upgradeability Intent", ["Just get me the best performance now",
                                                              "I want to upgrade the CPU in 3-4 years (High)"])
        workload = st.selectbox("Primary Workload", ["Just Gaming", "Streaming", "Heavy Editing"])
        library_size = st.selectbox("Game Library",
                                    ["Play 1-2 games at a time and uninstall", "Massive (Keep everything installed)"])

    submitted = st.form_submit_button("Run Expert Inference Engine")

# --- Execution Module ---
# CRITICAL FIX: Everything below this line is indented to ensure it only runs AFTER the button is clicked.
if submitted:
    # 1. Initialize Engine & Load Rules
    expert = PCBuilderExpertSystem()
    load_all_rules(expert)

    # 2. Add Base Facts from the UI
    expert.add_fact("Budget", budget)
    expert.add_fact("Target_Resolution", resolution)

    if preference != "No Preference":
        expert.add_fact("Preference", preference)
    if form_factor == "Small Form Factor (ITX)":
        expert.add_fact("Size", "Small")
    if "High" in upgrade_path:
        expert.add_fact("Upgrade_Path", "High")
    if workload != "Just Gaming":
        expert.add_fact("Workload", workload)
    if "Massive" in library_size:
        expert.add_fact("Library_Size", "Massive")

    # 3. Process Forward Chaining
    with st.spinner("Executing Forward Chaining Inference..."):
        expert.run_inference()
        hardware, explanations = expert.get_results()

    st.success("Inference Complete: Build Generated")

    # --- Display Hardware Results ---
    st.subheader("Recommended Architecture")
    cols = st.columns(3)
    col_idx = 0
    for component, part in hardware.items():
        # Using the markdown fix for formatting
        cols[col_idx % 3].markdown(f"**{component.replace('_', ' ')}**\n\n{part}")
        col_idx += 1

    # --- Display Explainable Reasoning Log ---
    st.divider()
    st.subheader("🧠 Explainable Reasoning Module")
    st.info("The system dynamically fired the following rules to deduce this architecture:")
    with st.expander("🧠 View Explainable Reasoning Log"):
        for log in explanations:
            # Prevents LaTeX rendering issues with the dollar sign
            safe_log = log.replace("$", r"\$")
            if "CONFLICT" in log:
                st.error(safe_log)
            else:
                st.markdown(f"- {safe_log}")