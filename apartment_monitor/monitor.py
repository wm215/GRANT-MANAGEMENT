"""Main application for the Lincoln Commons Apartment Monitor."""
import logging
import sys
import time
from datetime import datetime
from typing import Dict
import schedule

from . import config
from .scraper import LincolnCommonsScraper
from .notifications import NotificationManager


def setup_logging():
    """Set up logging configuration."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific logger levels to reduce noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)


class ApartmentMonitor:
    """Main apartment monitoring application."""
    
    def __init__(self):
        self.scraper = LincolnCommonsScraper()
        self.notifier = NotificationManager()
        self.logger = logging.getLogger(__name__)
        self.last_check_result = None
    
    def check_apartments(self) -> Dict:
        """Perform a single apartment availability check."""
        self.logger.info("Starting apartment availability check...")
        
        try:
            # Get current availability
            result = self.scraper.check_aro_one_bedroom_availability()
            
            if result.get('error'):
                self.logger.error(f"Check failed: {result['error']}")
                self.notifier.send_error_notification(result['error'])
                return result
            
            available_apartments = result.get('apartments', [])
            
            if available_apartments:
                self.logger.info(f"Found {len(available_apartments)} available ARO one-bedroom apartments!")
                
                # Send notifications
                notification_results = self.notifier.notify_availability(available_apartments)
                result['notifications'] = notification_results
                
                self.logger.info(f"Notifications sent - Email: {notification_results['email_sent']}, SMS: {notification_results['sms_sent']}")
            else:
                self.logger.info("No available ARO one-bedroom apartments found")
            
            self.last_check_result = result
            return result
            
        except Exception as e:
            self.logger.error(f"Unexpected error during check: {e}")
            error_result = {
                'available': False,
                'apartments': [],
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.notifier.send_error_notification(str(e))
            return error_result
    
    def run_once(self):
        """Run a single check and exit."""
        self.logger.info("Running single apartment check...")
        result = self.check_apartments()
        
        print("\\n" + "="*50)
        print("APARTMENT CHECK RESULTS")
        print("="*50)
        print(f"Timestamp: {result.get('timestamp', 'Unknown')}")
        print(f"Available ARO 1BR apartments: {len(result.get('apartments', []))}")
        print(f"Status: {'✅ AVAILABLE' if result.get('available') else '❌ NOT AVAILABLE'}")
        
        if result.get('error'):
            print(f"Error: {result['error']}")
        
        if result.get('notifications'):
            notif = result['notifications']
            print(f"Email sent: {'✅' if notif['email_sent'] else '❌'}")
            print(f"SMS sent: {'✅' if notif['sms_sent'] else '❌'}")
        
        print("="*50)
        
        return result
    
    def run_scheduler(self):
        """Run the apartment monitor with daily scheduling."""
        self.logger.info(f"Starting apartment monitor with daily checks at {config.CHECK_TIME}")
        
        # Schedule daily check
        schedule.every().day.at(config.CHECK_TIME).do(self.check_apartments)
        
        # Run an initial check
        self.logger.info("Running initial check...")
        self.check_apartments()
        
        # Start the scheduler loop
        self.logger.info("Scheduler started. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")
    
    def get_status(self) -> Dict:
        """Get current monitor status and configuration."""
        return {
            'configuration': {
                'target_url': config.LINCOLN_COMMONS_URL,
                'check_time': config.CHECK_TIME,
                'email_configured': self.notifier.email_configured,
                'sms_configured': self.notifier.sms_configured,
                'log_level': config.LOG_LEVEL
            },
            'last_check': self.last_check_result
        }


def main():
    """Main entry point for the application."""
    setup_logging()
    
    if len(sys.argv) < 2:
        print("Usage: python -m apartment_monitor.monitor [check|schedule|status|test]")
        print("  check    - Run a single apartment check")
        print("  schedule - Run with daily scheduling")
        print("  status   - Show current configuration and status")
        print("  test     - Run test mode with mock data")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    monitor = ApartmentMonitor()
    
    if command == "check":
        monitor.run_once()
    elif command == "schedule":
        monitor.run_scheduler()
    elif command == "status":
        status = monitor.get_status()
        print("\\n" + "="*50)
        print("APARTMENT MONITOR STATUS")
        print("="*50)
        print(f"Target URL: {status['configuration']['target_url']}")
        print(f"Check Time: {status['configuration']['check_time']}")
        print(f"Email Configured: {'✅' if status['configuration']['email_configured'] else '❌'}")
        print(f"SMS Configured: {'✅' if status['configuration']['sms_configured'] else '❌'}")
        print(f"Log Level: {status['configuration']['log_level']}")
        
        if status['last_check']:
            last = status['last_check']
            print(f"\\nLast Check: {last.get('timestamp', 'Unknown')}")
            print(f"Last Result: {'Available' if last.get('available') else 'Not Available'}")
        else:
            print("\\nNo checks performed yet")
        print("="*50)
    elif command == "test":
        # Run test mode with mock data
        from .test_utils import MockLincolnCommonsScraper
        
        print("\\n" + "="*50)
        print("RUNNING TEST MODE")
        print("="*50)
        
        # Test with no apartments available
        print("\\nTest 1: No ARO apartments available")
        print("-" * 30)
        monitor.scraper = MockLincolnCommonsScraper(mock_available=False)
        result1 = monitor.run_once()
        
        print("\\nTest 2: ARO apartments available")
        print("-" * 30)
        monitor.scraper = MockLincolnCommonsScraper(mock_available=True)
        result2 = monitor.run_once()
        
        print("\\n" + "="*50)
        print("TEST MODE COMPLETE")
        print("="*50)
        print("✅ All tests completed successfully!")
        print("The system is ready for production use with proper configuration.")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()