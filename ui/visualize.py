import streamlit as st
import pandas as pd
from utils.parser import sanitize_dict_for_table

def render_extracted_data(vitals: dict):
    """Visualizes extracted RFP JSON in clean Streamlit tables and sections."""

    def show_dict_section(title, data):
        if data:
            st.subheader(title)
            #df = pd.DataFrame.from_dict(data, orient="index", columns=["Value"])
            sanitized = sanitize_dict_for_table(data)
            df = pd.DataFrame.from_dict(sanitized, orient="index", columns=["Value"])
            st.table(df)

    def show_list_section(title, data):
        if data and isinstance(data, list):
            st.subheader(title)
            # Sanitize every dict in the list!
            sanitized_list = [
                sanitize_dict_for_table(row) if isinstance(row, dict) else row
                for row in data
            ]
            df = pd.DataFrame(sanitized_list)
            st.dataframe(df)
        # if data and isinstance(data, list):
        #     st.subheader(title)
        #     df = pd.DataFrame(data)
        #     st.dataframe(df)

    # Document Details
    show_dict_section("📄 Document Details", vitals.get("DocumentDetails"))

    # Buyer Details
    show_dict_section("🏢 Buyer Details", vitals.get("BuyerDetails"))

    # Vendor Details
    show_dict_section("🤝 Vendor Details", vitals.get("VendorDetails"))

    # Line Items
    show_list_section("📋 Line Items", vitals.get("LineItems"))

    # Financials
    show_dict_section("💰 Financials", vitals.get("Financials"))

    # Shipping Details
    show_dict_section("🚚 Shipping Details", vitals.get("ShippingDetails"))

    # Approval & Signatures
    show_dict_section("✍️ Approval & Signatures", vitals.get("ApprovalAndSignatures"))

    # Terms & Conditions
    tnc = vitals.get("TermsAndConditions")
    if tnc:
        st.subheader("📜 Terms & Conditions")
        url = tnc.pop("URL", None)
        if url:
            st.markdown(f"**URL:** [{url}]({url})")
        if tnc:
            sanitized_tnc = sanitize_dict_for_table(tnc)
            df_tnc = pd.DataFrame.from_dict(sanitized_tnc, orient="index", columns=["Value"])
            st.table(df_tnc)

    # Attachments
    atts = vitals.get("Attachments")
    if atts:
        st.subheader("📎 Attachments")
        for att_type, files in atts.items():
            st.markdown(f"**{att_type}:**")
            for fn in files:
                st.write(f"- {fn}")
