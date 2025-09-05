# 📦 Telegram Scraper Tool

A Python-based scraper built with [Telethon](https://github.com/LonamiWebs/Telethon) to collect data from **Telegram private chats, groups, and channels**.  
The tool extracts **messages, metadata, user information, and media**, and provides an option for **automatic translation** of messages using [deep_translator](https://pypi.org/project/deep-translator/) (Google Translate API or other supported services).

All collected data can be stored in a **pandas DataFrame** or exported to **CSV** for further analysis.

---

## ✨ Features

- 📥 Scrape messages, metadata, media, and user details from Telegram  
- 🌍 Automatic message translation (Google Translate, DeepL, etc. via `deep_translator`)  
- 📊 Export data to CSV or work directly with a pandas DataFrame  
- ⚡ Simple configuration and flexible usage  

---

## 🛠 Installation


Clone the repository and install dependencies. It is recommended to use a Python virtual environment:

```bash
# Clone the repository and change into the directory
git clone https://github.com/sergejlembke/telegram-scraper.git
cd telegram-scraper

# Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Required Python version:** 3.10 or higher

---

## 🚀 Usage

1. **Get your Telegram API credentials**  
   - Create an app at [my.telegram.org](https://my.telegram.org)  
   - Copy your `api_id` and `api_hash`

2. **Prepare your configuration**
    - Copy the provided `config.example.json` to `config.json` in the project root:
       ```bash
       cp config.example.json config.json
       # On Windows:
       copy config.example.json config.json
       ```
    - Open `config.json` and enter
       - your own Telegram API credentials
       - the desired translation settings
       - the export options (file format and append mode)
       - the chat IDs you want to scrape
    - Example `config.json`:
       ```json
      {
         "api_id": "YOUR_API_ID",
         "api_hash": "YOUR_API_HASH",
         "phone_number": "YOUR_PHONE_NUMBER",
         "translation": {
            "translate": true,
            "source_language": "auto",
            "target_language": "en"
         },
         "export_option": {
            "append": true,
            "format": ["json", "csv"]
         },
         "chats": [
            {"chat_name": "Example Private Channel", "chat_id": -100123456789},
            {"chat_name": "Example Public Channel", "chat_id": "@ExamplePublicChannelName"},
            {"chat_name": "Example Group Chat1", "chat_id": -100987654321},
            {"chat_name": "Example Group Chat2", "chat_id": "@ExampleGroupName"},
            {"chat_name": "Example Regular Chat1", "chat_id": 123456789},
            {"chat_name": "Example Regular Chat2", "chat_id": "@ExampleUserName"}
         ]
      }
       ```
   - To get the chat ID, login to the web version of Telegram and open the desired chat.
   - Click on the chat name at the top to open the chat info, where you can find the chat ID.
   - Insert the chat ID in the config.json in the following formats:
     - Private channels: '-100' followed by the channel ID (e.g., -100123456789)
     - Public channels: '@channelusername' (e.g., @PublicChannelName)
     - Group chats: '-100' followed by the group ID (e.g., -100987654321) or '@GroupName'
     - Regular chats: user ID or username as a string (e.g., '123456789' or '@UserName')


3. **Run the scraper**
   ```bash
   python main.py
   ```
---


## 📂 Example Output

CSV file structure:

| SENDER_NAME | SENDER_ID | MESSAGE_ID | DATE | MESSAGE | TRANSLATED_MESSAGE | MEDIA_PATH |
|-------------|-----------|------------|------|---------|--------------------------|------------|
| PythonLover | 123456789    | 742      | 2025-09-02 10:44:22+00:00  | Ich liebe Python       | I love Python                    | ./Scraped_Telegram_Data/PythonLover/PythonLover_photo_742.jpg |

---

## 📜 License

This project is licensed under the **AGPL-3.0 License** – see the [LICENSE]([LICENSE](https://www.gnu.org/licenses/agpl-3.0.en.html)) file for details.  

---

## 🔒 Disclaimer

⚠️ **Important:**  
This tool is intended **for educational and personal use only**.  
Please ensure that scraping and storing Telegram data complies with the **Telegram Terms of Service** and local privacy regulations.  
Do not use this project for unauthorized data collection.

---

## 🙌 Contribution

Pull requests, feature suggestions, and bug reports are welcome!  
Feel free to fork the repository and adapt the tool to your needs.  
