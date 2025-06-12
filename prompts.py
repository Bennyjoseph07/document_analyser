# prompts.py

VITALS_EXTRACTION_PROMPT = """
You are an AI assistant. Extract the following RFP structure in valid JSON format. The output must be only JSON without any markdown and any other prompts. Only return the JSON structure.

Use this structure:
{{
  "DocumentDetails": {{
    "DocumentType": "",          
    "DocumentNumber": "",
    "DocumentDate": "",
    "ReferenceNumbers": [],
    "Status": ""
  }},
  "BuyerDetails": {{
    "CompanyName": "",
    "Address": "",
    "ContactPerson": "",
    "Email": "",
    "Phone": "",
    "TRN": "",
    "BillingAddress": "",
    "ShippingAddress": ""
  }},
  "VendorDetails": {{
    "CompanyName": "",
    "Address": "",
    "ContactPerson": "",
    "Email": "",
    "Phone": "",
    "Fax": "",
    "TRN": ""
  }},
  "LineItems": [
    {{
      "LineNumber": "",
      "ItemCode": "",
      "Description": "",
      "Quantity": "",
      "UOM": "",
      "UnitPrice": "",
      "TotalPrice": "",
      "DeliveryDate": "",
      "RequisitionNumber": "",
      "Remarks": ""
    }}
  ],
  "Financials": {{
    "Currency": "",
    "SubTotal": "",
    "Discounts": "",
    "Taxes": {{
      "VATPercentage": "",
      "VATAmount": ""
    }},
    "TotalAmount": "",
    "PaymentTerms": "",
    "PricingModel": "",
    "BankDetails": ""
  }},
  "ShippingDetails": {{
    "ShipVia": "",
    "FOB": "",
    "Incoterm": "",
    "DeliveryTimeline": "",
    "ShipmentMethod": "",
    "PackingDetails": "",
    "TrackingRequired": ""
  }},
  "ApprovalAndSignatures": {{
    "AuthorizedBy": "",
    "AuthorizedEmail": "",
    "Signature": "",
    "ApprovedDate": ""
  }},
  "TermsAndConditions": {{
    "URL": "",
    "Warranty": "",
    "TerminationClause": "",
    "InspectionTerms": "",
    "PenaltyClause": "",
    "OtherNotes": []
  }},
  "Attachments": {{
    "SupportingDocuments": [],
    "DrawingsOrPlans": []
  }}
}}

Text:
{text}
"""

SECTION_PROMPTS = {
    "Executive Summary": "Write an Executive Summary for the following RFP:\n{text}",
    "Technical Solution": "Describe the Technical Solution based on the RFP:\n{text}",
    "Delivery Plan": "Create a Delivery Plan with key milestones and timelines:\n{text}",
    "Assumptions": "List the key Assumptions made in the proposal:\n{text}"
}
