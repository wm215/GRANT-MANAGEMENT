"""Notification system for apartment availability alerts."""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from . import config

logger = logging.getLogger(__name__)

# Try to import Twilio, but handle if it's not available
try:
    from twilio.rest import Client as TwilioClient
    TWILIO_AVAILABLE = True
except ImportError:
    logger.warning("Twilio not available. SMS notifications will be disabled.")
    TWILIO_AVAILABLE = False


class NotificationManager:
    """Manages email and SMS notifications."""
    
    def __init__(self):
        self.email_configured = self._check_email_config()
        self.sms_configured = self._check_sms_config()
    
    def _check_email_config(self) -> bool:
        """Check if email configuration is complete."""
        required = [config.EMAIL_USERNAME, config.EMAIL_PASSWORD, config.EMAIL_TO]
        configured = all(required)
        if not configured:
            logger.warning("Email configuration incomplete. Email notifications disabled.")
        return configured
    
    def _check_sms_config(self) -> bool:
        """Check if SMS configuration is complete."""
        if not TWILIO_AVAILABLE:
            return False
        
        required = [config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN, 
                   config.TWILIO_FROM_NUMBER, config.TWILIO_TO_NUMBER]
        configured = all(required)
        if not configured:
            logger.warning("SMS configuration incomplete. SMS notifications disabled.")
        return configured
    
    def send_email_notification(self, apartments: List[Dict]) -> bool:
        """Send email notification about available apartments."""
        if not self.email_configured:
            logger.warning("Email not configured. Skipping email notification.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_USERNAME
            msg['To'] = config.EMAIL_TO
            msg['Subject'] = "🏠 ARO One-Bedroom Apartment Available at Lincoln Commons!"
            
            # Create email body
            body = self._create_email_body(apartments)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT) as server:
                server.starttls()
                server.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
                server.send_message(msg)
            
            logger.info("Email notification sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    def send_sms_notification(self, apartments: List[Dict]) -> bool:
        """Send SMS notification about available apartments."""
        if not self.sms_configured:
            logger.warning("SMS not configured. Skipping SMS notification.")
            return False
        
        try:
            client = TwilioClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            
            message_body = self._create_sms_body(apartments)
            
            message = client.messages.create(
                body=message_body,
                from_=config.TWILIO_FROM_NUMBER,
                to=config.TWILIO_TO_NUMBER
            )
            
            logger.info(f"SMS notification sent successfully. Message SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
            return False
    
    def _create_email_body(self, apartments: List[Dict]) -> str:
        """Create HTML email body."""
        apartment_count = len(apartments)
        
        html_body = f"""
        <html>
        <body>
            <h2>🏠 Great News! ARO One-Bedroom Apartment(s) Available!</h2>
            <p>We found <strong>{apartment_count}</strong> available ARO one-bedroom apartment(s) at Lincoln Commons!</p>
            
            <h3>Details:</h3>
            <ul>
        """
        
        for i, apt in enumerate(apartments, 1):
            html_body += f"<li><strong>Unit {i}:</strong> ARO One-bedroom apartment available</li>"
        
        html_body += f"""
            </ul>
            
            <p><strong>Next Steps:</strong></p>
            <ol>
                <li>Visit the Lincoln Commons website: <a href="{config.LINCOLN_COMMONS_URL}">{config.LINCOLN_COMMONS_URL}</a></li>
                <li>Contact Lincoln Commons directly to inquire about the ARO one-bedroom units</li>
                <li>Act quickly as these units may be claimed fast!</li>
            </ol>
            
            <p><em>This is an automated notification from the Lincoln Commons Apartment Monitor.</em></p>
        </body>
        </html>
        """
        
        return html_body
    
    def _create_sms_body(self, apartments: List[Dict]) -> str:
        """Create SMS message body."""
        apartment_count = len(apartments)
        
        message = (f"🏠 ALERT: {apartment_count} ARO one-bedroom apartment(s) available at Lincoln Commons! "
                  f"Check now: {config.LINCOLN_COMMONS_URL}")
        
        return message
    
    def notify_availability(self, apartments: List[Dict]) -> Dict[str, bool]:
        """Send both email and SMS notifications."""
        results = {
            'email_sent': False,
            'sms_sent': False
        }
        
        if apartments:
            logger.info(f"Sending notifications for {len(apartments)} available apartments")
            results['email_sent'] = self.send_email_notification(apartments)
            results['sms_sent'] = self.send_sms_notification(apartments)
        else:
            logger.info("No apartments to notify about")
        
        return results
    
    def send_error_notification(self, error_message: str) -> bool:
        """Send notification about system errors."""
        if not self.email_configured:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_USERNAME
            msg['To'] = config.EMAIL_TO
            msg['Subject'] = "⚠️ Lincoln Commons Monitor Error"
            
            body = f"""
            <html>
            <body>
                <h2>⚠️ Lincoln Commons Apartment Monitor Error</h2>
                <p>The apartment monitoring system encountered an error:</p>
                <p><strong>Error:</strong> {error_message}</p>
                <p>Please check the system logs and configuration.</p>
                <p><em>Automated error notification</em></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT) as server:
                server.starttls()
                server.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
                server.send_message(msg)
            
            logger.info("Error notification sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")
            return False