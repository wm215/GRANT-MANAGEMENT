"""Web scraper for Lincoln Commons Apartments website."""
import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Optional
from . import config

logger = logging.getLogger(__name__)


class LincolnCommonsScraper:
    """Scraper for Lincoln Commons Apartments floorplans page."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
    
    def fetch_page(self) -> Optional[str]:
        """Fetch the floorplans page content."""
        try:
            logger.info(f"Fetching page: {config.LINCOLN_COMMONS_URL}")
            response = self.session.get(
                config.LINCOLN_COMMONS_URL,
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            logger.info("Successfully fetched page")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def parse_apartments(self, html_content: str) -> List[Dict]:
        """Parse apartment information from HTML content."""
        apartments = []
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Look for common apartment listing patterns
            # This may need adjustment based on actual website structure
            apartment_elements = soup.find_all(['div', 'section'], 
                                             class_=lambda x: x and any(
                                                 term in x.lower() for term in 
                                                 ['apartment', 'unit', 'floor', 'plan', 'listing']
                                             ))
            
            if not apartment_elements:
                # Try alternative selectors
                apartment_elements = soup.find_all(['div', 'article', 'section'])
            
            for element in apartment_elements:
                apartment_info = self._extract_apartment_info(element)
                if apartment_info:
                    apartments.append(apartment_info)
            
            logger.info(f"Found {len(apartments)} apartment listings")
            return apartments
            
        except Exception as e:
            logger.error(f"Error parsing apartments: {e}")
            return []
    
    def _extract_apartment_info(self, element) -> Optional[Dict]:
        """Extract apartment information from a single element."""
        try:
            text_content = element.get_text().lower()
            
            # Look for apartment information
            apartment_info = {
                'element_text': text_content,
                'is_one_bedroom': any(term in text_content for term in 
                                    ['1 bed', '1-bed', 'one bed', '1br', '1 br']),
                'is_aro': any(term in text_content for term in 
                            ['aro', 'affordable rental', 'affordable housing']),
                'available': any(term in text_content for term in 
                               ['available', 'vacant', 'ready']),
                'raw_html': str(element)
            }
            
            # Only return if it contains relevant information
            if any([apartment_info['is_one_bedroom'], apartment_info['is_aro']]):
                return apartment_info
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting apartment info: {e}")
            return None
    
    def check_aro_one_bedroom_availability(self) -> Dict:
        """Check for available ARO one-bedroom apartments."""
        result = {
            'available': False,
            'apartments': [],
            'error': None,
            'timestamp': None
        }
        
        try:
            from datetime import datetime
            result['timestamp'] = datetime.now().isoformat()
            
            html_content = self.fetch_page()
            if not html_content:
                result['error'] = "Failed to fetch page content"
                return result
            
            apartments = self.parse_apartments(html_content)
            
            # Filter for ARO one-bedroom apartments that are available
            aro_one_bedroom_available = []
            for apt in apartments:
                if (apt.get('is_one_bedroom') and 
                    apt.get('is_aro') and 
                    apt.get('available')):
                    aro_one_bedroom_available.append(apt)
            
            result['apartments'] = aro_one_bedroom_available
            result['available'] = len(aro_one_bedroom_available) > 0
            
            logger.info(f"Found {len(aro_one_bedroom_available)} available ARO one-bedroom apartments")
            
        except Exception as e:
            logger.error(f"Error checking availability: {e}")
            result['error'] = str(e)
        
        return result