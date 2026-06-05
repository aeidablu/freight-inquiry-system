import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
STAFF_EMAIL_1 = os.getenv("STAFF_EMAIL_1")
STAFF_EMAIL_2 = os.getenv("STAFF_EMAIL_2")

def send_staff_notification(inquiry_details: dict, reference_number: str) -> bool:
    try:
        subject = f"New Freight Inquiry - {reference_number}"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <div style="background: linear-gradient(90deg, #1e3a5f, #2196F3);
                        padding: 20px; border-radius: 10px; color: white;
                        text-align: center;">
                <h1>New Freight Inquiry</h1>
                <h2>Reference: {reference_number}</h2>
            </div>
           <div style="background: #f0fff0; padding: 20px;
                        border-radius: 10px; margin: 20px 0;">
                <h2 style="color: #1e3a5f;">Shipment Details</h2>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Name:</td>
                        <td style="padding: 8px;">{inquiry_details.get('customer_name', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Company:</td>
                        <td style="padding: 8px;">{inquiry_details.get('company_name', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Email:</td>
                        <td style="padding: 8px;">{inquiry_details.get('email', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Phone:</td>
                        <td style="padding: 8px;">{inquiry_details.get('phone', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Country:</td>
                        <td style="padding: 8px;">{inquiry_details.get('country', 'N/A')}</td>
                    </tr>
                    <tr style="background: #e8ffe8;">
                        <td style="padding: 8px; font-weight: bold;">Services Required:</td>
                        <td style="padding: 8px;">{inquiry_details.get('services_required', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Requirements:</td>
                        <td style="padding: 8px;">{inquiry_details.get('message', 'N/A')}</td>
                    </tr>
                </table>
            </div>
           <div style="background: #fff3cd; padding: 20px;
                        border-radius: 10px; margin: 20px 0;">
                <h2 style="color: #856404;">Please Add Your Rate</h2>
                <p>Reply to this email with the rate details:</p>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Ocean/Air Freight Rate:</td>
                        <td style="padding: 8px; background: white; border: 1px solid #ddd;">$____________</td>
                    </tr>
                    <tr style="background: #fffaed;">
                        <td style="padding: 8px; font-weight: bold;">Origin Charges:</td>
                        <td style="padding: 8px; background: white; border: 1px solid #ddd;">$____________</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Destination Charges:</td>
                        <td style="padding: 8px; background: white; border: 1px solid #ddd;">$____________</td>
                    </tr>
                    <tr style="background: #fffaed;">
                        <td style="padding: 8px; font-weight: bold;">Total Rate:</td>
                        <td style="padding: 8px; background: white; border: 1px solid #ddd;">$____________</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Transit Time:</td>
                        <td style="padding: 8px; background: white; border: 1px solid #ddd;">____________ days</td>
                    </tr>
                    <tr style="background: #fffaed;">
                        <td style="padding: 8px; font-weight: bold;">Valid Until:</td>
                        <td style="padding: 8px; background: white; border: 1px solid #ddd;">____________</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Remarks:</td>
                        <td style="padding: 8px; background: white; border: 1px solid #ddd;">____________</td>
                    </tr>
                </table>
            </div>
            <div style="text-align: center; margin: 20px 0;">
                <p style="color: #666;">Please respond within 5 minutes</p>
                <p style="color: #666;">Reference: {reference_number}</p>
                <p style="color: #666; font-size: 12px;">
                    ABC International Logistics | Karachi, Pakistan
                </p>
            </div>
        </body>
        </html>
        """

        staff_emails = [STAFF_EMAIL_1, STAFF_EMAIL_2]
        for staff_email in staff_emails:
            if staff_email:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = SENDER_EMAIL
                msg['To'] = staff_email
                msg.attach(MIMEText(html_body, 'html'))
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.sendmail(SENDER_EMAIL, staff_email, msg.as_string())

        print("Staff notification sent successfully!")
        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_customer_acknowledgment(
    customer_email: str,
    customer_name: str,
    reference_number: str
) -> bool:
    try:
        subject = f"Your Freight Inquiry Received - {reference_number}"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(90deg, #1e3a5f, #2196F3);
                        padding: 20px; border-radius: 10px; color: white;
                        text-align: center;">
                <h1>ABC International Logistics</h1>
            </div>
            <div style="padding: 30px;">
                <h2>Dear {customer_name},</h2>
                <p>Thank you for your freight inquiry. We have received your
                request and our team is reviewing it right now.</p>
                <div style="background: #f0f7ff; padding: 15px;
                            border-radius: 8px; border-left: 4px solid #2196F3;
                            margin: 20px 0;">
                    <h3>Your Reference Number:</h3>
                    <h2 style="color: #2196F3;">{reference_number}</h2>
                    <p>Please save this for future reference.</p>
                </div>
                <p>Our team will get back to you with the best rates
                <strong>within 5 minutes.</strong></p>
                <p>If you do not hear from us within 5 minutes, we will
                send you the best rates <strong>latest by tomorrow.</strong></p>
                <div style="background: #f9f9f9; padding: 15px;
                            border-radius: 8px; margin: 20px 0;">
                    <h3>Contact Us:</h3>
                    <p>Email: a.wahab.mu@gmail.com</p>
                    <p>Phone: +92-333-2191264</p>
                    <p>Karachi, Pakistan</p>
                </div>
                <p>Best Regards,</p>
                <p><strong>ABC International Logistics Team</strong></p>
            </div>
        </body>
        </html>
        """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = customer_email
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, customer_email, msg.as_string())

        print("Customer acknowledgment sent successfully!")
        return True

    except Exception as e:
        print(f"Customer email error: {e}")
        return False

def send_quote_to_customer(
    customer_email: str,
    customer_name: str,
    reference_number: str,
    pdf_path: str
) -> bool:
    """Send PDF quote to customer"""
    try:
        subject = f"Your Freight Quote - {reference_number}"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; 
                     max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(90deg, #1e3a5f, #2196F3);
                        padding: 20px; border-radius: 10px; 
                        color: white; text-align: center;">
                <h1>ABC International Logistics</h1>
            </div>
            <div style="padding: 30px;">
                <h2>Dear {customer_name},</h2>
                <p>Please find attached your freight quotation.</p>
                <div style="background: #f0f7ff; padding: 15px;
                            border-radius: 8px; 
                            border-left: 4px solid #2196F3;
                            margin: 20px 0;">
                    <h3>Quote Reference: {reference_number}</h3>
                    <p>This quote is valid for <strong>3 days</strong> 
                    from today.</p>
                </div>
                <p>Please review the attached PDF for full details 
                including rate breakdown, transit time, and 
                terms & conditions.</p>
                <p>To proceed, please reply to this email 
                or contact us directly.</p>
                <div style="background: #f9f9f9; padding: 15px;
                            border-radius: 8px; margin: 20px 0;">
                    <p>Email: a.wahab.mu@gmail.com</p>
                    <p>Phone: +92-333-2191264</p>
                    <p>Karachi, Pakistan</p>
                </div>
                <p>Best Regards,</p>
                <p><strong>ABC International Logistics Team</strong></p>
            </div>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = customer_email
        msg.attach(MIMEText(html_body, 'html'))

        # Attach PDF
        with open(pdf_path, 'rb') as f:
            from email.mime.application import MIMEApplication
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=f"Quote_{reference_number}.pdf"
            )
            msg.attach(pdf_attachment)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, customer_email, msg.as_string())

        print(f"Quote sent to customer successfully!")
        return True

    except Exception as e:
        print(f"Quote email error: {e}")
        return False
