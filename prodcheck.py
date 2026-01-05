#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

# 🔔 Webhooks with type
WEBHOOKS = [
    {
        "type": "discord",
        "url": "https://discord.com/api/webhooks/WEBHOOK_1"
    },
    {
        "type": "teams",
        "url": "https://outlook.office.com/webhook/WEBHOOK_2"
    }
]

# 🛒 Product URL
BESTBUY_URL = "https://www.bestbuy.ca/en-ca/product/ibuypower-slate-9-series-gaming-pc-white-intel-core-i9-14900kf-32gb-ram-2tb-ssd-rtx-5070-12gb-win-11/19306669"

def send_message(message):
    for webhook in WEBHOOKS:
        try:
            if webhook["type"] == "discord":
                payload = {"content": message}
            elif webhook["type"] == "teams":
                payload = {"text": message}

            response = requests.post(webhook["url"], json=payload)
            response.raise_for_status()

        except Exception as e:
            print(f"Error sending to {webhook['type']} webhook:", e)

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
                send_message(
                    "🟢 ITS HERE!!! — Item is in stock!\n" + BESTBUY_URL
                )
                return

        # Button missing or disabled = out of stock
        send_message(
            "🔴 Sadly, the product is still out of stock."
        )

    except Exception as e:
        print("Error during stock check:", e)

if __name__ == "__main__":
    check_stock()
