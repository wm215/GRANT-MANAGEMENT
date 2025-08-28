# GRANT MANAGEMENT & APARTMENT MONITORING

This repository contains two main projects:

## 1. Grant Management (UCRP Front Step Replacement)

Administrative and documentation repository for the United Church of Rogers Park (UCRP) $250,000 DCEO grant for front step replacement project. See `grant_action_plan.md` for detailed deliverables and timeline.

### Key Files:
- `grant_action_plan.md` - Complete action plan and deliverables tracking
- `Documents/` - Grant-related documentation and templates
- `Grant - W.melendez/` - Project-specific files and tracking

## 2. ARO Apartment Availability Monitor

Automated monitoring system for ARO (Affordable Rental Opportunity) one-bedroom apartments at Lincoln Commons (https://www.lincolncommonapartments.com/floorplans).

### Features:
- **Web Scraping**: Monitors Lincoln Commons website for ARO one-bedroom availability
- **Notifications**: Sends email/SMS alerts when units become available
- **Automation**: Runs periodically via GitHub Actions (hourly checks)

### Quick Start:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Notifications**:
   - Copy `src/config.py.example` to `src/config.py`
   - Add your email/SMS credentials and recipient information

3. **Run Manually**:
   ```bash
   python src/apartment_scraper.py
   ```

4. **Automated Monitoring**:
   - The scraper runs automatically every hour via GitHub Actions
   - Configure notification settings in `src/config.py`

### Project Structure:
```
src/
├── apartment_scraper.py    # Main scraping script
├── config.py              # Configuration settings
└── config.py.example      # Example configuration

.github/workflows/
└── apartment_monitor.yml  # Automated scheduling workflow
```

### Dependencies:
- `requests` - HTTP requests for web scraping
- `beautifulsoup4` - HTML parsing
- `schedule` - Task scheduling (for local runs)
- `smtplib` - Email notifications (built-in)

### Configuration:
Set up your notification preferences in `src/config.py`:
- Email SMTP settings
- SMS provider settings (optional)
- Recipient contact information
- Monitoring frequency preferences

---

## License
This project is for personal/organizational use in monitoring apartment availability and managing grant documentation.