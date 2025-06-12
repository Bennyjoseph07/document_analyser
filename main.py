import streamlit as st
import json
from utils.parser import parse_pdf, parse_docx,flatten_for_csv
from utils.generator import extract_vitals, generate_section
from ui.visualize import render_extracted_data
import pandas as pd

# Load persona hints
try:
    with open("data/persona_hints.json") as f:
        persona_hints = json.load(f)
except FileNotFoundError:
    persona_hints = {}
    st.warning("persona_hints.json not found. Using default hints.")

# Page config
st.set_page_config(page_title="AI RFP Assistant", layout="wide")
st.title("AI RFP Assistant")
st.markdown("Upload an RFP document and let the AI extract structured details and generate proposal drafts.")

# Sections
sections = ["Executive Summary", "Technical Solution", "Delivery Plan", "Assumptions"]



# Initialize session state
if "extract_status" not in st.session_state:
    st.session_state.extract_status = "not_started"
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = ""
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None
if "rfp_text" not in st.session_state:
    st.session_state.rfp_text = ""
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# Initialize section states
for section in sections:
    if f"{section}_status" not in st.session_state:
        st.session_state[f"{section}_status"] = "not_started"
    if f"{section}_draft" not in st.session_state:
        st.session_state[f"{section}_draft"] = ""

# Status mappings
extract_status_map = {
    "not_started": "Yet to extract",
    "in_progress": "Extracting...",
    "done": "Extracted",
    "error": "Error"
}
section_status_map = {
    "not_started": "Yet to generate",
    "in_progress": "Generating...",
    "done": "Generated",
    "error": "Error"
}

# Function to render sidebar status
def render_sidebar_status():
    st.sidebar.markdown("### Extraction Status")
    extract_status_text = extract_status_map.get(st.session_state.extract_status, "Unknown")
    st.sidebar.markdown(f"**RFP Details:** {extract_status_text}")
    
    st.sidebar.markdown("### Section Status")
    for sec in sections:
        status = section_status_map.get(st.session_state.get(f"{sec}_status", "not_started"), "Unknown")
        st.sidebar.markdown(f"**{sec}:** {status}")

# Sidebar – Upload
st.sidebar.header("Upload RFP Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])

# Process file upload
if uploaded_file:
    current_file_name = uploaded_file.name
    
    # Check if it's a new file or same file
    if (current_file_name != st.session_state.uploaded_file_name or 
        not st.session_state.file_processed):
        
        try:
            # Parse the file
            file_ext = uploaded_file.name.split(".")[-1].lower()
            if file_ext == "pdf":
                rfp_text = parse_pdf(uploaded_file)
            elif file_ext == "docx":
                rfp_text = parse_docx(uploaded_file)
            else:
                st.error("Unsupported file format")
                st.stop()
            
            # Update session state
            st.session_state.rfp_text = rfp_text
            st.session_state.uploaded_file_name = current_file_name
            st.session_state.file_processed = True
            
            # Reset extraction and section states for new file
            st.session_state.extract_status = "not_started"
            st.session_state.extracted_data = None
            for section in sections:
                st.session_state[f"{section}_status"] = "not_started"
                st.session_state[f"{section}_draft"] = ""
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.stop()

# Render sidebar status
if uploaded_file:
    render_sidebar_status()

# Main content
if uploaded_file and st.session_state.file_processed:
    # Tabs
    tab1, tab2, tab3 = st.tabs(["RFP Preview", "Extract Details", "Proposal Drafts"])

    # Tab 1 – RFP Preview
    with tab1:
        st.subheader("RFP Content")
        st.text_area("Extracted Text", st.session_state.rfp_text, height=400, disabled=True)
        st.info(f"File: {st.session_state.uploaded_file_name} | Characters: {len(st.session_state.rfp_text):,}")

    # Tab 2 – Extract Details
    with tab2:
        st.subheader("Extract Structured RFP Details")

        # Extract button
        if st.session_state.extract_status == "not_started":
            if st.button("Extract RFP Details", type="primary"):
                st.session_state.extract_status = "in_progress"
                st.rerun()

        # Handle extraction process
        elif st.session_state.extract_status == "in_progress":
            with st.spinner("Extracting RFP details..."):
                try:
                    result = extract_vitals(st.session_state.rfp_text)
                    parsed = json.loads(result)
                    st.session_state.extracted_data = parsed
                    st.session_state.extract_status = "done"
                    st.rerun()
                except json.JSONDecodeError:
                    st.session_state.extract_status = "error"
                    st.error("The AI returned invalid JSON. Please try again.")
                    if 'result' in locals():
                        st.code(result)
                    st.rerun()
                except Exception as e:
                    st.session_state.extract_status = "error"
                    st.error(f"Error during extraction: {str(e)}")
                    st.rerun()

        # Show results
        elif st.session_state.extract_status == "done":
            st.success("Extraction completed successfully!")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                with st.expander("View Extracted JSON", expanded=True):
                    render_extracted_data(st.session_state.extracted_data)
                    #st.json(st.session_state.extracted_data)      
            with col2:
                if st.button("Re-extract"):
                    st.session_state.extract_status = "not_started"
                    st.session_state.extracted_data = None
                    st.rerun()
                # --- Download Buttons ---
                st.markdown("#### Download Extracted Data")
                extracted_json_str = json.dumps(st.session_state.extracted_data, indent=2, ensure_ascii=False)
                st.download_button(
                    label="Download as TXT (JSON)",
                    data=extracted_json_str,
                    file_name="rfp_extracted.json.txt",
                    mime="text/plain",
                    key="download_json_txt"
                )
                extracted_df = flatten_for_csv(st.session_state.extracted_data)
                csv_bytes = extracted_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download as CSV (Flattened)",
                    data=csv_bytes,
                    file_name="rfp_extracted.csv",
                    mime="text/csv",
                    key="download_csv"
                )

        elif st.session_state.extract_status == "error":
            st.error("Extraction failed. Please try again.")
            if st.button("Retry Extraction"):
                st.session_state.extract_status = "not_started"
                st.rerun()

    # Tab 3 – Proposal Drafts
    with tab3:
        st.subheader("Generate Proposal Sections")
        
        # Check if extraction is done
        if st.session_state.extract_status != "done":
            st.warning("Please extract RFP details first before generating proposal sections.")
        else:
            for section in sections:
                with st.expander(f"{section}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        current_status = st.session_state.get(f"{section}_status", "not_started")
                        
                        # Generate button
                        if current_status == "not_started":
                            if st.button(f"Generate {section}", key=f"btn_{section}"):
                                st.session_state[f"{section}_status"] = "in_progress"
                                st.rerun()
                        
                        # Handle generation process
                        elif current_status == "in_progress":
                            with st.spinner(f"Generating {section}..."):
                                try:
                                    draft = generate_section(section, st.session_state.rfp_text)
                                    st.session_state[f"{section}_draft"] = draft
                                    st.session_state[f"{section}_status"] = "done"
                                    st.rerun()
                                except Exception as e:
                                    st.session_state[f"{section}_status"] = "error"
                                    st.error(f"Error generating {section}: {str(e)}")
                                    st.rerun()
                        
                        # Show generated content
                        elif current_status == "done":
                            st.success(f"{section} generated successfully!")
                            
                            # Editable text area
                            draft_text = st.text_area(
                                f"{section} (Editable)", 
                                st.session_state[f"{section}_draft"], 
                                key=f"text_{section}",
                                height=200
                            )
                            
                            # Update session state if text is modified
                            if draft_text != st.session_state[f"{section}_draft"]:
                                st.session_state[f"{section}_draft"] = draft_text
                            
                            # Action buttons
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                if st.button(f"Regenerate {section}", key=f"regen_{section}"):
                                    st.session_state[f"{section}_status"] = "not_started"
                                    st.session_state[f"{section}_draft"] = ""
                                    st.rerun()
                            with btn_col2:
                                if st.download_button(
                                    f"Download {section}",
                                    draft_text,
                                    file_name=f"{section.lower().replace(' ', '_')}.txt",
                                    mime="text/plain",
                                    key=f"download_{section}"
                                ):
                                    st.success(f"{section} downloaded!")
                        
                        elif current_status == "error":
                            st.error(f"Error generating {section}")
                            if st.button(f"Retry {section}", key=f"retry_{section}"):
                                st.session_state[f"{section}_status"] = "not_started"
                                st.rerun()
                    
                    with col2:
                        st.markdown("#### Persona Guidance")
                        hint = persona_hints.get(section, "No specific guidance available for this section.")
                        st.info(hint)

else:
    st.warning("Please upload a PDF or Word document to begin.")
    # Render empty sidebar status
    st.sidebar.markdown("### Status")
    st.sidebar.info("Upload a file to see extraction and generation status")

# Footer
st.markdown("---")
st.markdown("**AI RFP Assistant** - Streamline your proposal generation process")