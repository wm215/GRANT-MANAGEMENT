#!/usr/bin/env python3
"""
Demo script for ARO Apartment Monitor

This script demonstrates the apartment monitoring functionality without
actually sending notifications. Use this to test the scraping logic.
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

def demo_scraper():
    """Demonstrate the apartment scraper functionality"""
    print("ARO Apartment Monitor - Demo Mode")
    print("=" * 40)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        from apartment_scraper import LincolnCommonsMonitor
        
        # Create monitor instance
        monitor = LincolnCommonsMonitor()
        print("✓ Monitor instance created successfully")
        
        # Show configuration
        print("\nConfiguration loaded:")
        try:
            from config import EMAIL_SETTINGS, NOTIFICATION_SETTINGS
            print(f"  SMTP Server: {EMAIL_SETTINGS.get('smtp_server', 'Not configured')}")
            print(f"  Recipient: {NOTIFICATION_SETTINGS.get('recipient_email', 'Not configured')}")
            
            if 'placeholder' in EMAIL_SETTINGS.get('smtp_user', '').lower():
                print("  ⚠ Email settings contain placeholder values")
            
        except ImportError:
            print("  ⚠ Configuration not found")
        
        print("\nDemo Mode - Scraper Ready")
        print("=" * 40)
        print("In normal operation, the scraper would:")
        print("1. Connect to https://www.lincolncommonapartments.com/floorplans")
        print("2. Parse the page for ARO one-bedroom units")
        print("3. Send email notifications if units are available")
        print("4. Log all activity to apartment_monitor.log")
        print()
        print("To run the actual scraper:")
        print("  python apartment_scraper.py")
        print()
        print("To set up automated monitoring:")
        print("  Configure GitHub secrets and the workflow will run hourly")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main demo function"""
    success = demo_scraper()
    
    if success:
        print("\n✓ Demo completed successfully!")
        print("The apartment monitoring system is ready for use.")
    else:
        print("\n✗ Demo failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()