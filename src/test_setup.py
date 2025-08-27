#!/usr/bin/env python3
"""
Test script for ARO Apartment Monitor setup

This script validates the project setup and configuration.
Run this after setting up your config.py file.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import requests
        print("✓ requests module available")
    except ImportError:
        print("✗ requests module missing - run: pip install -r requirements.txt")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ beautifulsoup4 module available")
    except ImportError:
        print("✗ beautifulsoup4 module missing - run: pip install -r requirements.txt")
        return False
    
    try:
        import schedule
        print("✓ schedule module available")
    except ImportError:
        print("✗ schedule module missing - run: pip install -r requirements.txt")
        return False
    
    return True

def test_config():
    """Test configuration file"""
    print("\nTesting configuration...")
    
    try:
        from config import EMAIL_SETTINGS, NOTIFICATION_SETTINGS, MONITORING_SETTINGS
        print("✓ Configuration file loaded successfully")
        
        # Check for placeholder values
        if 'placeholder' in EMAIL_SETTINGS.get('smtp_user', '').lower():
            print("⚠ Warning: Email settings contain placeholder values")
            print("  Please update src/config.py with your actual email settings")
        
        if 'example.com' in NOTIFICATION_SETTINGS.get('recipient_email', ''):
            print("⚠ Warning: Recipient email contains placeholder values")
            print("  Please update src/config.py with actual recipient email")
        
        return True
        
    except ImportError as e:
        print(f"✗ Configuration file error: {e}")
        print("  Please ensure src/config.py exists and is properly formatted")
        return False

def test_network():
    """Test network connectivity to Lincoln Commons"""
    print("\nTesting network connectivity...")
    
    try:
        import requests
        url = "https://www.lincolncommonapartments.com/floorplans"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✓ Successfully connected to Lincoln Commons website")
            return True
        else:
            print(f"⚠ Warning: Received status code {response.status_code} from website")
            return True  # Not necessarily a failure
            
    except Exception as e:
        print(f"✗ Network connectivity error: {e}")
        print("  Check your internet connection")
        return False

def main():
    """Run all tests"""
    print("ARO Apartment Monitor - Setup Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test configuration
    if not test_config():
        all_passed = False
    
    # Test network
    if not test_network():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! The apartment monitor is ready to use.")
        print("\nNext steps:")
        print("1. Update src/config.py with your email settings")
        print("2. Run: python src/apartment_scraper.py")
    else:
        print("✗ Some tests failed. Please address the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()