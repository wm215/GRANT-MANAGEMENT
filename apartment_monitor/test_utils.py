"""Test utilities for the apartment monitor."""
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class MockLincolnCommonsScraper:
    """Mock scraper for testing purposes."""
    
    def __init__(self, mock_available=False):
        self.mock_available = mock_available
    
    def check_aro_one_bedroom_availability(self) -> Dict:
        """Mock apartment availability check."""
        logger.info("Running mock apartment check...")
        
        if self.mock_available:
            apartments = [{
                'element_text': 'aro one bedroom apartment available now',
                'is_one_bedroom': True,
                'is_aro': True,
                'available': True,
                'raw_html': '<div>Mock ARO 1BR Available</div>'
            }]
        else:
            apartments = []
        
        result = {
            'available': len(apartments) > 0,
            'apartments': apartments,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Mock check complete. Found {len(apartments)} apartments")
        return result


def create_mock_html_with_apartments():
    """Create mock HTML content with apartment listings."""
    return """
    <html>
    <head><title>Lincoln Commons - Floorplans</title></head>
    <body>
        <div class="apartment-listing">
            <h2>Studio Apartments</h2>
            <div class="unit">Studio - Market Rate - Available</div>
        </div>
        
        <div class="apartment-listing">
            <h2>One Bedroom Apartments</h2>
            <div class="unit">1 Bedroom - Market Rate - Waitlist Only</div>
            <div class="unit">1 BR ARO Affordable Rental Option - Available Now!</div>
        </div>
        
        <div class="apartment-listing">
            <h2>Two Bedroom Apartments</h2>
            <div class="unit">2 Bedroom - Market Rate - Available</div>
        </div>
    </body>
    </html>
    """


def create_mock_html_no_apartments():
    """Create mock HTML content without available ARO apartments."""
    return """
    <html>
    <head><title>Lincoln Commons - Floorplans</title></head>
    <body>
        <div class="apartment-listing">
            <h2>Studio Apartments</h2>
            <div class="unit">Studio - Market Rate - Waitlist Only</div>
        </div>
        
        <div class="apartment-listing">
            <h2>One Bedroom Apartments</h2>
            <div class="unit">1 Bedroom - Market Rate - Waitlist Only</div>
        </div>
        
        <div class="apartment-listing">
            <h2>Two Bedroom Apartments</h2>
            <div class="unit">2 Bedroom - Market Rate - Waitlist Only</div>
        </div>
    </body>
    </html>
    """