import requests
from bs4 import BeautifulSoup
import smtplib
import os
import lxml

# Email Details.
SMTP = "smtp.gmail.com"
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
sender_email = os.environ["sender_email"]

# Product to Track.
URL = ("https://www.amazon.com/Apple-iPhone-14-128GB-Midnight/dp/B0BN733951/ref=sr_1_2?crid=3HF4UCBWKEO52&keywords="
       "iphone%2B14&qid=1705316253&sprefix=iPhone%2Caps%2C2178&sr=8-2&th=1")

# MY HTTP  HEADER
headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.com/',
    'accept-language': "en-US,en-GB;q=0.9,en;q=0.8,nl;q=0.7",
}

response = requests.get(url=URL, headers=headers)
response.raise_for_status()
website = response.text
# print(website)

soup = BeautifulSoup(website, "lxml")
# print(soup.prettify())

price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
# print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()

BUY_PRICE = 580

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"
    with smtplib.SMTP(SMTP, port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=sender_email,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8")
        )
