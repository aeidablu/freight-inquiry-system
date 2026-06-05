import streamlit as st
from agent import run_agent, extract_inquiry_details
from email_service import send_staff_notification, send_customer_acknowledgment, send_quote_to_customer
from email_parser import check_staff_reply
from quote_generator import generate_quote_pdf
import os
from langchain_core.messages import HumanMessage, AIMessage
import json
from datetime import datetime
import time
import random

# ── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Freight Inquiry System",
    page_icon="🚢",
    layout="wide"
)

# Custom CSS for better look
st.markdown("""
<style>
    .main { padding: 0; }
    .stButton > button {
        background: linear-gradient(90deg, #1e3a5f, #2196F3);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #2196F3, #1e3a5f);
    }
    .form-box {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .success-box {
        background: #f0fff0;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Countries List ───────────────────────────────────────────────────
COUNTRIES = [
    "Select Country",
    "Afghanistan", "Australia", "Bahrain", "Bangladesh", "Belgium",
    "Brazil", "Canada", "China", "Denmark", "Egypt", "Finland",
    "France", "Germany", "Greece", "Hong Kong", "India", "Indonesia",
    "Iran", "Iraq", "Italy", "Japan", "Jordan", "Kazakhstan",
    "Kenya", "Kuwait", "Malaysia", "Maldives", "Mexico", "Morocco",
    "Netherlands", "New Zealand", "Nigeria", "Norway", "Oman",
    "Pakistan", "Philippines", "Poland", "Portugal", "Qatar",
    "Romania", "Russia", "Saudi Arabia", "Singapore", "South Africa",
    "South Korea", "Spain", "Sri Lanka", "Sweden", "Switzerland",
    "Taiwan", "Thailand", "Turkey", "UAE", "UK", "Ukraine",
    "USA", "Uzbekistan", "Vietnam", "Yemen"
]

# ── Services List ────────────────────────────────────────────────────
SERVICES = [
    "Sea Freight - LCL (Less than Container Load)",
    "Sea Freight - FCL (Full Container Load)",
    "Air Freight",
    "Customs Clearance",
    "Door to Door Delivery",
    "Warehousing",
    "Import Services",
    "Export Services",
]

# ── Initialize Session State ─────────────────────────────────────────
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "inquiry_details" not in st.session_state:
    st.session_state.inquiry_details = {}
if "inquiry_time" not in st.session_state:
    st.session_state.inquiry_time = None
if "reference_number" not in st.session_state:
    st.session_state.reference_number = ""

# Header with logo
col1, col2 = st.columns([1, 4])

#with col1:
#    st.image("cirrus.jpg", width=110)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a5f, #2196F3);
                padding: 25px; border-radius: 15px; text-align: center;
                color: white;">
        <h1 style="margin: 0; font-size: 35px;">
            Welcome to ABC International Logistics! 👋
        </h1>
        <p style="margin: 5px 0 0 0; font-size: 18px; opacity: 0.9;">
            Your trusted freight forwarding partner in World Wide.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Main Content ─────────────────────────────────────────────────────
if not st.session_state.form_submitted:

    col_left, col_form, col_right = st.columns([1, 4, 1])

    with col_form:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #1e3a5f;">📦 Request a Freight Quote</h2>
            <p style="color: #666;">
                Fill in the form below and our team will respond within 5 minutes.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Form Fields ──────────────────────────────────────────────
        col_a, col_b = st.columns(2)

        with col_a:
            name = st.text_input("👤 Full Name *", placeholder="John Smith")

        with col_b:
            company = st.text_input("🏢 Company Name *",
                                    placeholder="ABC Trading Co.")

        col_c, col_d = st.columns(2)

        with col_c:
            email = st.text_input("📧 Email Address *",
                                  placeholder="john@company.com")

        with col_d:
            phone = st.text_input("📱 Contact Number *",
                                  placeholder="+92-300-1234567")

        col_e, col_f = st.columns(2)

        with col_e:
            country = st.selectbox("🌍 Country *", COUNTRIES)

        with col_f:
            services = st.multiselect(
                "🚢 Services Required *",
                SERVICES,
                placeholder="Select services..."
            )

        message = st.text_area(
            "💬 Additional Information",
            placeholder="Please share cargo details, origin/destination, "
                       "container type, commodity, required date, "
                       "or any special requirements...",
            height=120
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Submit Button ────────────────────────────────────────────
        submit = st.button("🚀 Submit Freight Inquiry", type="primary")

        if submit:
            # Validation
            errors = []
            if not name.strip():
                errors.append("Full Name is required")
            if not company.strip():
                errors.append("Company Name is required")
            if not email.strip() or "@" not in email:
                errors.append("Valid Email Address is required")
            if not phone.strip():
                errors.append("Contact Number is required")
            if country == "Select Country":
                errors.append("Please select a Country")
            if not services:
                errors.append("Please select at least one Service")

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Generate reference number
                ref_number = f"FR-2026-{random.randint(1000, 9999)}"

                # Build inquiry details
                inquiry_details = {
                    "customer_name": name,
                    "company_name": company,
                    "email": email,
                    "phone": phone,
                    "country": country,
                    "services_required": ", ".join(services),
                    "message": message,
                    "reference_number": ref_number,
                    "shipment_direction": "N/A",
                    "origin_port": "N/A",
                    "destination_port": country,
                    "service_type": ", ".join(services),
                    "incoterms": "N/A",
                    "shipment_type": "N/A",
                    "container_size": "N/A",
                    "container_type": "N/A",
                    "number_of_containers": "N/A",
                    "cargo_weight_kg": "N/A",
                    "commodity": message,
                    "dangerous_goods": "N/A",
                    "special_handling": "N/A",
                    "insurance_required": "N/A",
                    "required_date": "N/A",
                    "date_flexible": "N/A",
                    "status": "pending"
                }

                with st.spinner("Submitting your inquiry..."):
                    # Send staff notification
                    send_staff_notification(inquiry_details, ref_number)

                    # Send customer acknowledgment
                    send_customer_acknowledgment(name, email, ref_number)

                # Save to session
                st.session_state.form_submitted = True
                st.session_state.inquiry_details = inquiry_details
                st.session_state.reference_number = ref_number
                st.session_state.inquiry_time = time.time()
                st.rerun()

else:
    # ── Success Screen ───────────────────────────────────────────────
    col_left, col_center, col_right = st.columns([1, 4, 1])

    with col_center:
        st.markdown(f"""
        <div style="background: #f0fff0; padding: 30px;
                    border-radius: 15px; text-align: center;
                    border: 2px solid #4CAF50; margin: 20px 0;">
            <h1 style="color: #4CAF50;">✅ Inquiry Submitted!</h1>
            <p style="font-size: 18px; color: #333;">
                Thank you <b>{st.session_state.inquiry_details.get('customer_name', '')}!</b>
            </p>
            <p style="color: #666;">
                Your inquiry has been sent to our team successfully.
            </p>
            <div style="background: white; padding: 15px;
                        border-radius: 10px; margin: 15px 0;
                        border: 1px solid #ddd;">
                <h3 style="color: #1e3a5f;">Your Reference Number:</h3>
                <h2 style="color: #2196F3; font-size: 28px;">
                    {st.session_state.reference_number}
                </h2>
                <p style="color: #666; font-size: 13px;">
                    Please save this for future reference.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Timer ────────────────────────────────────────────────────
        if st.session_state.inquiry_time:
            elapsed = time.time() - st.session_state.inquiry_time
            remaining = 300 - elapsed

            if remaining > 0:
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                st.info(f"⏱️ Our team is reviewing your inquiry. "
                       f"Expected response in: **{minutes}m {seconds}s**")

                # Check staff reply
                ref = st.session_state.reference_number
                rates = check_staff_reply(ref)

                if rates and rates.get('ocean_freight', '0') != '0':
                    pdf_path = f"quote_{ref}.pdf"
                    generate_quote_pdf(
                        st.session_state.inquiry_details,
                        rates,
                        pdf_path
                    )
                    send_quote_to_customer(
                        st.session_state.inquiry_details.get('email', ''),
                        st.session_state.inquiry_details.get(
                            'customer_name', ''),
                        ref,
                        pdf_path
                    )
                    st.success("🎉 Quote has been sent to your email!")
                    st.balloons()
                else:
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning(
                    "⏰ Our team is still preparing your quote. "
                    "We will send you the best rates **latest by tomorrow.**"
                )

        # ── Summary ──────────────────────────────────────────────────
        st.markdown("### 📋 Your Inquiry Summary")
        details = st.session_state.inquiry_details

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**👤 Name:** {details.get('customer_name', 'N/A')}")
            st.markdown(f"**🏢 Company:** {details.get('company_name', 'N/A')}")
            st.markdown(f"**📧 Email:** {details.get('email', 'N/A')}")
            st.markdown(f"**📱 Phone:** {details.get('phone', 'N/A')}")

        with col2:
            st.markdown(f"**🌍 Country:** {details.get('country', 'N/A')}")
            st.markdown(f"**🚢 Services:** {details.get('services_required', 'N/A')}")
            st.markdown(f"**💬 Message:** {details.get('message', 'N/A')}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── New Inquiry Button ────────────────────────────────────────
        if st.button("🔄 Submit Another Inquiry"):
            st.session_state.form_submitted = False
            st.session_state.inquiry_details = {}
            st.session_state.inquiry_time = None
            st.session_state.reference_number = ""
            st.rerun()

# ── Footer ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background: #1e3a5f; padding: 20px;
            border-radius: 10px; text-align: center; color: white;">
    <p style="margin: 0; font-size: 14px;">
        📍 PECHS Shahrah-e-Faisal, Karachi, Pakistan
    </p>
    <p style="margin: 5px 0 0 0; font-size: 14px;">
        📧 a.wahab.mu@gmail.com | 📱 +92-333-2191264
    </p>
    <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.7;">
        © 2026 ABC International Logistics. All Rights Reserved.
    </p>
</div>
""", unsafe_allow_html=True)