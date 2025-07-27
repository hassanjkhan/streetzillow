# apt_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Replace these configuration values with yours
TARGET_SITE = "https://example.com/apartments"  # Change to your desired site.
EMAIL_TO = "youremail@example.com"
EMAIL_FROM = "yourbot@example.com"
EMAIL_PASSWORD = "your-email-app-password"

def scrape_listings():
    listings = []
    today = datetime.now()
    two_days_ago = today - timedelta(days=2)
    
    # Example: Fetch the page and parse it (update URL and parsing as needed)
    response = requests.get(TARGET_SITE)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # This is dummy logic; update selectors based on the actual site's HTML.
    for listing_item in soup.find_all("div", class_="listing"):
        title = listing_item.find("h2").get_text(strip=True)
        link = listing_item.find("a")["href"]
        sqft = listing_item.find("span", class_="sqft").get_text(strip=True)
        posted_date_str = listing_item.find("span", class_="posted-date").get_text(strip=True)
        # Convert posted_date_str to datetime (you might need to change the format)
        posted_date = datetime.strptime(posted_date_str, "%Y-%m-%d")
        
        # Example features—adjust these fields based on the data available:
        features = {
            "washer_dryer": "Washer/Dryer" in listing_item.get_text(),
            "dishwasher": "Dishwasher" in listing_item.get_text(),
            "elevator": "Elevator" in listing_item.get_text(),
            "walk_up": "Walk-up" in listing_item.get_text(),
        }
        
        # Example commute info (you might incorporate Google Maps API later)
        commute_time = "Unknown"  # Placeholder
        
        if posted_date >= two_days_ago:
            listings.append({
                "title": title,
                "link": link,
                "sqft": sqft,
                "posted_date": posted_date_str,
                "commute_time": commute_time,
                **features
            })
    
    return listings

def send_email(listings):
    if not listings:
        return
    
    body = "\n\n".join(
        f"{l['title']}\n{l['link']}\n{l['sqft']} sqft | Washer/Dryer: {l['washer_dryer']} | "
        f"Dishwasher: {l['dishwasher']} | Elevator: {l['elevator']} | Walk-up: {l['walk_up']}\n"
        f"Commute: {l['commute_time']}\nPosted: {l['posted_date']}"
        for l in listings
    )
    
    msg = MIMEText(body)
    msg["Subject"] = "New Apartment Listings"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    # Using Gmail's SMTP server (adjust if using another email provider)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    listings = scrape_listings()
    send_email(listings)

if __name__ == "__main__":
    main()
