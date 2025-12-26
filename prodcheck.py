#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = "https://discord.com/api/webhooks/1454190741743079455/GPJI0Q1ycmaK3v1Yph_Rf33qbvLZazBHMi-93wenkq54uUVIPZzaUbLRFHgj3h-MFoyH"
BESTBUY_URL = "https://www.bestbuy.ca/en-ca/product/ibuypower-slate-9-series-gaming-pc-white-intel-core-i9-14900kf-32gb-ram-2tb-ssd-rtx-5070-12gb-win-11/19306669"

def send_discord_message(message):
    try:
        response = requests.post(WEBHOOK_URL, json={"content": message})
        response.raise_for_status()
    except Exception as e:
        print("Error sending Discord message:", e)

def check_stock():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(BESTBUY_URL, headers=headers)
        response.raise_for_status()  # Raises an error if HTTP status != 200
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for the Add to Cart button
        button = soup.find("button", {"class": "add-to-cart-button"})

        if button:
            button_text = button.get_text(strip=True)
            disabled = button.has_attr("disabled")

            if not disabled and "Add to Cart" in button_text:
                send_discord_message("🟢 ITS HERE!!! — Item is in stock!\n" + BESTBUY_URL)
                return

        # If button not found or disabled
        send_discord_message("🔴 Sadly, the product is still out of stock.")

    except Exception as e:
        print("Error during stock check:", e)

if __name__ == "__main__":
    check_stock()
