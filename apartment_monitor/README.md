# Lincoln Commons Apartment Monitor

A Python-based system that monitors the Lincoln Commons Apartments website for available ARO (Affordable Rental Option) one-bedroom apartments and sends notifications when they become available.

## Features

- **Web Scraping**: Automatically checks the Lincoln Commons floorplans page for apartment availability
- **Email Notifications**: Sends HTML email alerts when ARO one-bedroom units are available
- **SMS Notifications**: Sends text message alerts via Twilio
- **Daily Scheduling**: Runs automated checks at a configured time each day
- **Error Handling**: Comprehensive error handling with notification of system issues
- **Logging**: Detailed logging for monitoring and debugging

## Installation

1. **Install Python Dependencies**:
   ```bash
   cd apartment_monitor
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration values
   ```

## Configuration

### Email Setup (Gmail example)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for the apartment monitor
3. Add your credentials to `.env`:
   ```
   EMAIL_USERNAME=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_TO=recipient@example.com
   ```

### SMS Setup (Twilio)
1. Sign up for a Twilio account
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Add credentials to `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_FROM_NUMBER=+1234567890
   TWILIO_TO_NUMBER=+0987654321
   ```

## Usage

### Run a Single Check
```bash
python -m apartment_monitor check
```

### Run with Daily Scheduling
```bash
python -m apartment_monitor schedule
```

### Check Status and Configuration
```bash
python -m apartment_monitor status
```

## Deployment Options

### Local Deployment
Run the scheduler in the background:
```bash
nohup python -m apartment_monitor schedule &
```

### Cron Job (Linux/macOS)
Add to crontab for daily checks at 9 AM:
```bash
crontab -e
# Add this line:
0 9 * * * cd /path/to/apartment_monitor && python -m apartment_monitor check
```

### Cloud Deployment
The system can be deployed to cloud platforms like:
- **AWS EC2**: Run as a background service
- **Google Cloud Compute**: Use with Cloud Scheduler
- **Heroku**: Deploy with Heroku Scheduler add-on
- **DigitalOcean Droplet**: Run as a systemd service

## System Requirements

- Python 3.7+
- Internet connection
- Email account (for email notifications)
- Twilio account (for SMS notifications)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Email Issues**: Check that 2FA is enabled and you're using an app password
3. **SMS Issues**: Verify Twilio credentials and phone number format (+1234567890)
4. **Web Scraping Issues**: The website structure may change; check logs for parsing errors

### Logs
Check the log file (`apartment_monitor.log`) for detailed error information:
```bash
tail -f apartment_monitor.log
```

## Contributing

This system is designed to be easily extensible. You can:
- Add new notification channels
- Modify the scraping logic for website changes
- Add additional apartment criteria
- Enhance error handling

## Legal Notice

This tool is for personal use only. Please respect the Lincoln Commons website's terms of service and rate limits. The scraper includes appropriate delays and user agent strings to be respectful of the target website.