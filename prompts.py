# prompts.py

VITALS_EXTRACTION_PROMPT = """
You are an AI assistant. Extract the following RFP structure in valid JSON format from the provided RFP text.

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
    "Executive Summary": """You are writing an executive summary for an RFP response on behalf of a technology service provider.
 
Based on the following inputs, draft a compelling, 2–3 paragraph executive summary. The tone should be professional, confident, and aligned with a business persona.
 
Inputs:
- RFP title
- Customer/industry
- High-level solution strategy
- Key differentiators of the bidder (e.g., experience, tech stack, innovation) for the following RFP:\n{text}""",
    
    
    "Technical Solution": """You are a senior solution architect drafting the technical approach section for an RFP response.
 
Use the following inputs to generate a detailed solution description covering architecture, tech stack, scalability, security, integration, and any relevant standards or frameworks.
 
Tone: Confident, technical, structured.
 
Inputs:
- RFP category: (e.g., Healthcare Portal Modernization)
- Core tech stack: (e.g., React + FastAPI + PostgreSQL)
- Compliance: (e.g., FHIR, HIPAA, OWASP)
- Deployment model: (e.g., cloud-native, Kubernetes, Azure)
- Integration: (e.g., EMR, SAP, HL7) based on the RFP:\n{text}""",

    "Delivery Plan": """You are a pre-sales manager drafting the delivery plan for an RFP response.
 
Write a 3–5 paragraph delivery plan including:
- Project phases (Initiation, Design, Development, Testing, Go-Live)
- Timeline overview (without hard dates)
- Resource types (e.g., architect, developers, QA)
- Communication and governance model
 
Make it sound reliable, flexible, and professional.:\n{text}""",


    "Assumptions": """You are a solution architect reviewing an RFP.
 
Based on the below content, generate 5 to 10 smart and professional clarification questions that the bidder can send to the client. These questions should seek clarification on ambiguous areas, missing details, or conflicting information.
 :\n{text}"""
}
