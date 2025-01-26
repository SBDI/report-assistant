import streamlit as st
from report_assistant import graph
from configuration import Configuration
import os

# Set page config
st.set_page_config(
    page_title="Report mAIstro",
    page_icon="📊",
    layout="centered"
)

# Initialize session state
if 'report' not in st.session_state:
    st.session_state.report = None

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    model_choice = st.selectbox(
        "AI Model",
        ["llama3-70b-8192", "mixtral-8x7b-32768"],
        index=0
    )
    truncation_level = st.slider(
        "Truncation Level (%)", 
        min_value=50, 
        max_value=100, 
        value=85,
        help="Higher values preserve more content but increase API usage"
    )

# Main interface
st.title("📊 Report mAIstro")
st.caption("Generate professional reports with AI-powered research")

# Input form
with st.form("report_form"):
    topic = st.text_input("Report Topic", placeholder="Enter your topic...")
    report_type = st.selectbox(
        "Report Type",
        ["Business Strategy", "Comparative Analysis", "Technical Guide", "Trend Report"]
    )
    
    submitted = st.form_submit_button("Generate Report")
    
    if submitted:
        with st.spinner("🔍 Researching and writing your report..."):
            try:
                # Convert report type to config
                report_type_map = {
                    "Business Strategy": "business_strategy",
                    "Comparative Analysis": "comparative_analysis",
                    "Technical Guide": "how_to",
                    "Trend Report": "recent_events"
                }
                
                # Invoke the graph
                result = graph.invoke({
                    "topic": topic,
                    "configurable": {
                        "report_structure": report_type_map[report_type],
                        "max_input_tokens": int(8192 * (truncation_level/100))
                    }
                })
                
                st.session_state.report = result['final_report']
                st.success("✅ Report generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")

# Display report
if st.session_state.report:
    st.subheader("Generated Report")
    with st.expander("View Full Report"):
        st.markdown(st.session_state.report)
    
    # Download button
    st.download_button(
        label="📥 Download Report",
        data=st.session_state.report,
        file_name=f"{topic.replace(' ', '_')}_report.md",
        mime="text/markdown"
    )

# Add footer
st.markdown("---")
st.markdown("Powered by [Groq](https://groq.com/) | Built with [LangGraph](https://langchain-ai.github.io/langgraph/)")