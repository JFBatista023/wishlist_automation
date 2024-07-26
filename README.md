# Product Price Monitor

This script monitors product prices on AliExpress (for now...) and sends notifications via Telegram and WhatsApp. It uses Selenium to scrape product prices from specified URLs and compares them against predefined alert prices. If a product's price falls below the alert price, a message is sent via WhatsApp using the pywhatkit library. Telegram messages containing the current prices of all products are sent periodically.

## Setup Guide

### Prerequisites

- Python 3.9+

### Steps

1. **Clone the Repository**

    ```bash
    git clone git@github.com:JFBatista023/wishlist_automation.git
    cd wishlist_automation
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**

    - On Windows:

      ```bash
      .\venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Setup Environment Variables**

    - Create a `.env` file in the root directory of the project.
    - Copy the contents of `.env-example` to `.env`.

      ```bash
      cp .env-example .env
      ```

    - Fill in your details in the `.env` file:

      ```plaintext
      TELEGRAM_BOT_TOKEN=your_telegram_bot_token
      TELEGRAM_CHAT_ID=your_telegram_chat_id
      WHATSAPP_NUMBER=your_whatsapp_number
      ```

### Telegram Bot Setup

1. Create a new bot on Telegram by talking to the [BotFather](https://telegram.me/botfather).
2. Get the bot token from the BotFather and add it to your `.env` file as `TELEGRAM_BOT_TOKEN`.
3. Get your chat ID by starting a chat with your bot.

### Execution

To run the script, simply execute the following command:

```bash
python main.py
