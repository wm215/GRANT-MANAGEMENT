#!/usr/bin/env python3
"""
ARO Apartment Availability Monitor for Lincoln Commons

This script monitors the Lincoln Commons website for ARO (Affordable Rental Opportunity)
one-bedroom apartment availability and sends notifications when units become available.

Website: https://www.lincolncommonapartments.com/floorplans
"""

import requests
import time
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

# Import configuration
try:
    from config import (
        EMAIL_SETTINGS,
        NOTIFICATION_SETTINGS,
        MONITORING_SETTINGS
    )
except ImportError:
    print("Error: config.py not found. Please copy config.py.example to config.py and configure your settings.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('apartment_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LincolnCommonsMonitor:
    """Monitor Lincoln Commons website for ARO apartment availability"""
    
    def __init__(self):
        self.base_url = "https://www.lincolncommonapartments.com/floorplans"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def fetch_page(self) -> Optional[BeautifulSoup]:
        """Fetch and parse the floorplans page"""
        try:
            logger.info(f"Fetching page: {self.base_url}")
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            logger.info("Successfully fetched and parsed page")
            return soup
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def find_aro_units(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Find ARO one-bedroom units from the parsed page"""
        aro_units = []
        
        try:
            # Look for floorplan containers - this may need adjustment based on actual site structure
            floorplan_containers = soup.find_all(['div', 'section'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['floorplan', 'unit', 'apartment', 'plan']
            ))
            
            for container in floorplan_containers:
                # Look for one-bedroom indicators
                text_content = container.get_text().lower()
                if 'bedroom' in text_content or '1br' in text_content or '1 br' in text_content:
                    # Check for ARO indicators
                    if any(keyword in text_content for keyword in ['aro', 'affordable', 'rental opportunity']):
                        unit_info = self.extract_unit_info(container)
                        if unit_info:
                            aro_units.append(unit_info)
            
            logger.info(f"Found {len(aro_units)} ARO one-bedroom units")
            return aro_units
            
        except Exception as e:
            logger.error(f"Error parsing ARO units: {e}")
            return []
    
    def extract_unit_info(self, container) -> Optional[Dict[str, str]]:
        """Extract unit information from a container element"""
        try:
            unit_info = {}
            
            # Extract unit name/number
            title_elem = container.find(['h1', 'h2', 'h3', 'h4'], string=lambda x: x and 'bedroom' in x.lower())
            if title_elem:
                unit_info['name'] = title_elem.get_text().strip()
            
            # Extract availability status
            availability_elem = container.find(string=lambda x: x and any(
                keyword in x.lower() for keyword in ['available', 'vacant', 'ready']
            ))
            if availability_elem:
                unit_info['availability'] = availability_elem.strip()
            
            # Extract rent price
            price_elem = container.find(string=lambda x: x and '$' in x)
            if price_elem:
                unit_info['price'] = price_elem.strip()
            
            # Extract square footage
            sqft_elem = container.find(string=lambda x: x and ('sq ft' in x.lower() or 'sqft' in x.lower()))
            if sqft_elem:
                unit_info['sqft'] = sqft_elem.strip()
            
            return unit_info if unit_info else None
            
        except Exception as e:
            logger.error(f"Error extracting unit info: {e}")
            return None
    
    def send_notification(self, available_units: List[Dict[str, str]]):
        """Send notification about available units"""
        if not available_units:
            return
        
        try:
            subject = f"ARO Units Available at Lincoln Commons - {len(available_units)} unit(s)"
            
            # Build email body
            body = f"""
ARO One-Bedroom Units Available at Lincoln Commons!

Found {len(available_units)} available ARO one-bedroom unit(s):

"""
            
            for i, unit in enumerate(available_units, 1):
                body += f"""
Unit {i}:
- Name: {unit.get('name', 'N/A')}
- Availability: {unit.get('availability', 'N/A')}
- Price: {unit.get('price', 'N/A')}
- Square Footage: {unit.get('sqft', 'N/A')}

"""
            
            body += f"""
Check the website for more details and to apply:
{self.base_url}

This alert was generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            self.send_email(subject, body)
            logger.info(f"Notification sent for {len(available_units)} available units")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    def send_email(self, subject: str, body: str):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SETTINGS['smtp_user']
            msg['To'] = NOTIFICATION_SETTINGS['recipient_email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(EMAIL_SETTINGS['smtp_server'], EMAIL_SETTINGS['smtp_port'])
            server.starttls()
            server.login(EMAIL_SETTINGS['smtp_user'], EMAIL_SETTINGS['smtp_password'])
            
            text = msg.as_string()
            server.sendmail(EMAIL_SETTINGS['smtp_user'], NOTIFICATION_SETTINGS['recipient_email'], text)
            server.quit()
            
            logger.info("Email notification sent successfully")
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
    
    def check_availability(self):
        """Main method to check for available ARO units"""
        logger.info("Starting apartment availability check")
        
        soup = self.fetch_page()
        if not soup:
            logger.error("Failed to fetch page, skipping check")
            return
        
        available_units = self.find_aro_units(soup)
        
        if available_units:
            logger.info(f"Found {len(available_units)} available ARO units!")
            self.send_notification(available_units)
        else:
            logger.info("No ARO one-bedroom units currently available")
        
        logger.info("Apartment availability check completed")

def main():
    """Main function"""
    try:
        monitor = LincolnCommonsMonitor()
        monitor.check_availability()
        
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main()