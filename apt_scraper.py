import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

print("✅ Script started...")

# 🔒 Hardcoded credentials for testing
EMAIL_FROM = "streetzillow@gmail.com"
EMAIL_PASSWORD = "lmxtdfbgyfkuqpbj"  # Your app password, not regular one
EMAIL_TO = "streetzillow@gmail.com"

def scrape_listings():
    print("🔍 Scraping listings...")

    listings = []
    today = datetime.now()
    two_days_ago = today - timedelta(days=2)

    print("ℹ️ Using dummy data for now...")
    listings.append({
        "title": "Fake 2BR in East Village",
        "link": "https://example.com/fake-listing",
        "sqft": 750,
        "washer_dryer": True,
        "dishwasher": True,
        "elevator": False,
        "walk_up": True,
        "posted_date": today.strftime("%Y-%m-%d"),
        "commute_time": "15 mins to 770 Broadway",
    })

    print(f"📦 Found {len(listings)} total listings")

    recent = [
        l for l in listings
        if datetime.strptime(l["posted_date"], "%Y-%m-%d") >= two_days_ago
    ]
    print(f"🧼 Filtered to {len(recent)} listings from past 2 days")
    return recent

def send_email(listings):
    if not listings:
        print("📭 No new listings to email.")
        return

    print("📤 Sending email...")

    body = "\n\n".join(
        f"{l['title']}\n{l['link']}\n{l['sqft']} sqft | Washer/Dryer: {l['washer_dryer']} | "
        f"Dishwasher: {l['dishwasher']} | Elevator: {l['elevator']} | Walk-up: {l['walk_up']}\n"
        f"Commute: {l['commute_time']}"
        for l in listings
    )

    msg = MIMEText(body)
    msg["Subject"] = "🆕 New Apartment Listings"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

if __name__ == "__main__":
    try:
        print("🚀 Running apt_scraper main flow...")
        listings = scrape_listings()
        send_email(listings)
        print("🎉 Script finished successfully.")
    except Exception as err:
        print("💥 Script crashed with error:", err)
