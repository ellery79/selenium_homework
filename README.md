# Library Book Scraper

## Author
Name: Poon Ho Chuen
Class number: 15
Course: CT290DS003 Python 網站框架開發助理證書
Institution: 港專職業訓練學院

## Description
Library Book Scraper is a Python script developed as part of the CT290DS003 Python 網站框架開發助理證書 course at 港專職業訓練學院. It automates the process of extracting book information from a library website using Selenium WebDriver to navigate through paginated book listings and scrape details such as title, author, publication year, and other metadata.

## Features
- Scrapes book details from multiple pages
- Extracts comprehensive metadata for each book
- Exports data to a CSV file for easy analysis
- Utilizes headless browser for efficient scraping

## Requirements
- Python 3.12.7
- Selenium WebDriver
- Chrome WebDriver

## Installation
1. Clone this repository:
``` shell
git clone https://github.com/yourusername/library-book-scraper.git
```

2. Navigate to the project directory:

cd library-book-scraper

3. Install the required packages:

pip install selenium
livecodeserver

4. Download the appropriate version of ChromeDriver for your system and place it in the `./chromedriver/` directory.

## Usage
Run the script with the following command:

python scraper.py
livecodeserver

The scraped data will be saved in `scraped_books.csv` in the same directory.

## Configuration
You can modify the target URL in the `main()` function of `scraper.py` if you want to scrape a different library website.

## Output
The script generates a CSV file named `scraped_books.csv` with the following columns:
- Title
- District
- Author
- Copy ID
- Publication Year
- Publisher
- Call Number
- Edition
- New Release

## Educational Context
This project was developed as part of the curriculum for CT290DS003 Python 網站框架開發助理證書 at 港專職業訓練學院. It serves as a practical application of web scraping techniques and Python programming skills learned during the course.

## License
This project is licensed under a custom Educational Project License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This script is for educational purposes only. Make sure you have permission to scrape the target website and comply with their terms of service.