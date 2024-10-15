# Library Book Scraper

## Author
- **Name**: Poon Ho Chuen
- **Class number**: 15
- **Course**: CT290DS003 Python 網站框架開發助理證書
- **Institution**: 港專職業訓練學院

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
git clone git@github.com:ellery79/selenium_homework.git
```

2. Navigate to the project directory:
``` shell
cd selenium_homework
```

3. Install the required packages:

``` shell
pip install -r requirements.txt
```

4. Download the appropriate version of ChromeDriver for your system and place it in the `./chromedriver/` directory.
Download address: https://googlechromelabs.github.io/chrome-for-testing/

## Usage
Run the script with the following command:
``` shell
python scraper.py
```

The scraped data will be saved in `scraped_books.csv` in the same directory.


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

## Acknowledgments
- 衛龍老師 for project guidance
- Generative AI tools for assistance with coding challenges and problem-solving
