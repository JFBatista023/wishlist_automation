import os
import time

from pydantic import BaseModel
from typing import Optional

import pywhatkit as kit
import telegram
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils import *


class Product(BaseModel):
    name: str
    url: str
    alert_price: Optional[float] = None


# Edit the list with the products you want
products = [
    Product(name="Redmi Watch 3 Active",
            url="https://pt.aliexpress.com/item/1005005655136135.html?gatewayAdapt=glo2bra", alert_price=160.00),
    Product(name="Attack Shark K86 10k vendidos",
            url="https://pt.aliexpress.com/item/1005006086958220.html?gatewayAdapt=glo2bra", alert_price=260.00),
    Product(name="AULA F75",
            url="https://pt.aliexpress.com/item/1005006907892071.html?gatewayAdapt=glo2bra", alert_price=260.00),
    Product(name="Attach Shark K86 1k vendidos",
            url="https://pt.aliexpress.com/item/1005006086926348.html?gatewayAdapt=glo2bra", alert_price=260.00),
    Product(name="Redragon KS82-B",
            url="https://pt.aliexpress.com/item/1005005483117627.html?gatewayAdapt=glo2bra", alert_price=260.00),
    Product(name="Teclado XVN",
            url="https://pt.aliexpress.com/item/1005005943274023.html?spm=a2g0s.8937460.appWishlistRecommend.4"
                ".322bZvzPZvzPUj&gps-id=appWishlistRecommend&scm=1007.25197.281209.0&scm_id=1007.25197.281209.0&scm"
                "-url=1007.25197.281209.0&pvid=06e2693e-83f6-404b-bd20-460a70e5930a&_t=gps-id:appWishlistRecommend,"
                "scm-url:1007.25197.281209.0,pvid:06e2693e-83f6-404b-bd20-460a70e5930a,"
                "tpp_buckets:668%232846%238110%231995&pdp_npi=4%40dis%21BRL%21530.73%21271.06%21%21%21648.73%21331.32"
                "%21%402103080c17219213335303011e8fd3%2112000034960732300%21rec%21BR%213086941037%21",
            alert_price=260.00)]

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER')


def fetch_product_price(url: str, driver) -> float:
    driver.get(url)

    discount_per_piece_xpath = '/html/body/div[6]/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[2]/span/span'
    raw_price_xpath = '/html/body/div[6]/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/span'
    tax_price_xpath = '/html/body/div[6]/div/div[1]/div/div[1]/div[1]/div[2]/div[3]/a'

    discount_per_piece_element = get_element(driver, By.XPATH, discount_per_piece_xpath, retry=1, wait_time=6) # It is normal for the result of this function to give Timeout
    if discount_per_piece_element is not None:
        raw_price_xpath = '/html/body/div[6]/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]/span'
        tax_price_xpath = '/html/body/div[6]/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/a'

    raw_price = get_element_text(driver, By.XPATH, raw_price_xpath)
    tax_price = get_element_text(driver, By.XPATH, tax_price_xpath)

    price = float(raw_price.split('R$')[1].replace(',', '.')) + float(tax_price.split('R$')[1].split(' ')[0].replace(',', '.'))

    return round(price, 2)


async def send_telegram_message(message: str):
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    async with bot:
        await bot.send_message(text=message, chat_id=TELEGRAM_CHAT_ID)
    print('Telegram message sent successfully!')


def send_whatsapp_message(message: str):
    kit.sendwhatmsg_instantly(WHATSAPP_NUMBER, message)
    print('Whatsapp message sent successfully!')


async def main(driver):
    while True:
        telegram_message = ""
        whatsapp_message = ""

        for product in products:
            price = fetch_product_price(product.url, driver)
            telegram_message += f"{product.name}: R$ {price}\n"

            if product.alert_price and price <= product.alert_price:
                whatsapp_message += f"Atenção! {product.name} está agora por R$ {price}\n"
                whatsapp_message += f"Aqui está o link: {product.url}\n"

        await send_telegram_message(telegram_message)

        if whatsapp_message:
            send_whatsapp_message(whatsapp_message)

        time.sleep(3600)


if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = 'none'
    chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
    asyncio.run(main(chrome_driver))
    chrome_driver.quit()
