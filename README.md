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

2. **Run the scraper**
   ```bash
   python scraper.py

    Choose your export option

        csv file

        pandas DataFrame (for further analysis in Python)
   ```

3. **Choose your export option**
   - `csv` file  
   - `pandas DataFrame` (for further analysis in Python)
  

---

## ⚙️ Configuration

Edit the `config.json` (or set environment variables) to specify:

- `api_id`, `api_hash` (Telegram credentials)  
- Target chats / groups / channels  
- Translation service (`google`, `deepl`, etc.)  
- Export format (`csv`, `dataframe`)  

---

## 📂 Example Output

CSV file structure:

| chat_id | sender | message | timestamp   | language | translation | media_path |
|---------|--------|---------|-------------|----------|-------------|------------|
| 123456  | Alice  | Hello   | 2025-08-20  | en       | Hallo       | ./media/... |

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
