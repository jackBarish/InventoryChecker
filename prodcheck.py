#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup

#webhooks
WEBHOOK_URLS = [
    "https://discord.com/api/webhooks/1454190741743079455/GPJI0Q1ycmaK3v1Yph_Rf33qbvLZazBHMi-93wenkq54uUVIPZzaUbLRFHgj3h-MFoyH",
    "https://interpublic.webhook.office.com/webhookb2/f9ab9cbb-59cb-40ee-b6ac-d0e94d86b829@d026e4c1-5892-497a-b9da-ee493c9f0364/IncomingWebhook/956f1dc1b1b34347a6c02f46d3aa79bf/83b7dad1-0d35-4489-815f-e0db897df861/V2TXvwLrDaXxemFnEuYYI0m5d85vMbW5SGhShlKbCVWlQ1"
]

#Product URL
BESTBUY_URL = "https://www.bestbuy.ca/en-ca/product/ibuypower-slate-9-series-gaming-pc-white-intel-core-i9-14900kf-32gb-ram-2tb-ssd-rtx-5070-12gb-win-11/19306669"

def send_discord_message(message):
    for webhook_url in WEBHOOK_URLS:
        try:
            response = requests.post(webhook_url, json={"content": message})
            response.raise_for_status()
        except Exception as e:
            print(f"Error sending Discord message to {webhook_url}: {e}")

def check_stock():
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(BESTBUY_URL, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Look for the Add to Cart button
        button = soup.find("button", {"class": "add-to-cart-button"})

        if button:
            button_text = button.get_text(strip=True)
            disabled = button.has_attr("disabled")

            if not disabled and "Add to Cart" in button_text:
                send_discord_message(
                    "🟢 ITS HERE!!! — Item is in stock!\n" + BESTBUY_URL
                )
                return

        # Button missing or disabled = out of stock
        send_discord_message(
            "🔴 Sadly, the product is still out of stock."
        )

    except Exception as e:
        print("Error during stock check:", e)

if __name__ == "__main__":
    check_stock()
