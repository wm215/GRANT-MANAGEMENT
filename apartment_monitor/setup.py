#!/usr/bin/env python3
"""Deployment and setup script for the Lincoln Commons Apartment Monitor."""
import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print the setup banner."""
    print("="*60)
    print("🏠 LINCOLN COMMONS APARTMENT MONITOR SETUP")
    print("="*60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing dependencies...")
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        requirements_file = script_dir / "requirements.txt"
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    script_dir = Path(__file__).parent
    env_file = script_dir / ".env"
    example_file = script_dir / ".env.example"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if example_file.exists():
        try:
            import shutil
            shutil.copy(example_file, env_file)
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your actual configuration")
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("❌ .env.example file not found")
        return False

def test_installation():
    """Test the installation."""
    print("\n🧪 Testing installation...")
    try:
        # Add the parent directory to Python path for import
        import sys
        parent_dir = str(Path(__file__).parent.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        # Import the module
        import apartment_monitor
        print("✅ Module import successful")
        
        # Run status command
        from apartment_monitor.monitor import ApartmentMonitor
        monitor = ApartmentMonitor()
        status = monitor.get_status()
        print("✅ Status check successful")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for configuration."""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Edit the .env file with your email and SMS credentials:")
    print("   - EMAIL_USERNAME and EMAIL_PASSWORD (Gmail app password)")
    print("   - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and phone numbers")
    print()
    print("2. Test the system:")
    print("   python -m apartment_monitor test")
    print()
    print("3. Run a real check:")
    print("   python -m apartment_monitor check")
    print()
    print("4. For daily monitoring:")
    print("   python -m apartment_monitor schedule")
    print()
    print("5. Check status anytime:")
    print("   python -m apartment_monitor status")
    print()
    print("📖 See README.md for detailed configuration instructions")
    print("="*60)

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Create .env file
    if not create_env_file():
        return 1
    
    # Test installation
    if not test_installation():
        return 1
    
    # Print next steps
    print_next_steps()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())