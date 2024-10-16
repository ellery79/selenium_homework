"""
Library Book Scraper

This module provides functionality to scrape book details from a library website
using Selenium WebDriver. It extracts information such as title, author, 
publication year, and other metadata from book listings across paginated pages.

The main components of this module are:
- WebDriver setup for headless Chrome browser
- Functions to extract text and book details from HTML elements
- CSV writing capability for storing scraped data
- Pagination handling to scrape books across multiple pages

Dependencies:
- selenium: For web scraping and browser automation
- csv: For writing scraped data to CSV files

Usage:
Run this script directly to start the scraping process. The results will be
saved in a CSV file named 'scraped_books.csv' in the same directory.

Note: Ensure that the Chrome WebDriver executable (chromedriver) is available
in the './chromedriver/' directory relative to this script.

This version (1.1) includes optimizations for memory efficiency, processing
books one at a time instead of storing all book details in memory at once.

Author: Poon Ho Chuen
Date: 16 Oct 2024
Version: 1.1
"""

import csv
from functools import partial

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    TimeoutException
)


def setup_driver():
    """Initialize and return a headless Chrome WebDriver."""
    options = Options()
    options.add_argument("--headless")
    service = Service("./chromedriver/chromedriver")
    return webdriver.Chrome(service=service, options=options)


def extract_text(element, selector, split_delimiter=": "):
    """
    Extract and split the text from a child element based on a CSS selector.

    Parameters:
        element: The parent Selenium WebElement.
        selector: The CSS selector string to locate the child element.
        split_delimiter: The delimiter to split the text.

    Returns:
        The part of the text after the delimiter or an empty string if not found.
    """
    try:
        text = element.find_element(
            By.CSS_SELECTOR, selector).find_element(By.XPATH, "..").text
        return text.split(split_delimiter, 1)[-1]
    except NoSuchElementException:
        return ""


def extract_book_details(selectors, book):
    """
    Extract detailed information from a single book element.
    
    Parameters:
        selectors: A dictionary mapping detail keys to CSS selectors.
        book: The Selenium WebElement representing a book.

    Returns:
        A dictionary containing the extracted book details.
    """
    extract = partial(extract_text, book)
    details = {
        key: (book.find_element(By.CSS_SELECTOR, selector).text if key ==
              "title" else extract(selector))
        for key, selector in selectors.items()
        if key != "new_release"
    }
    details["new_release"] = bool(book.find_elements(
        By.CSS_SELECTOR, selectors["new_release"]))
    return details


def fetch_books(driver):
    """Generator to fetch all book elements across paginated pages."""
    wait = WebDriverWait(driver, 10)
    while True:
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".card.listing-preview")))
        yield from driver.find_elements(By.CSS_SELECTOR, ".card.listing-preview")

        try:
            next_button = driver.find_element(
                By.XPATH, '//a[normalize-space()="»"]')
            if next_button.is_enabled() and next_button.is_displayed():
                next_button.click()
                wait.until(EC.staleness_of(next_button))
            else:
                break
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            break


def write_books_to_csv(filename, fieldnames, books):
    """
    Write book details to a CSV file and return the count of books written.

    Parameters:
        filename: The name of the CSV file to write to.
        fieldnames: A list of field names for the CSV header.
        books: An iterable of dictionaries containing book details.

    Returns:
        The number of books written to the CSV file.
    """
    count = 0
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            print(book)
            writer.writerow(book)
            count += 1
    return count


def main():
    """
    Main function to orchestrate the scraping process.
    
    This function sets up the WebDriver, defines the CSS selectors for book details,
    fetches books from the website, extracts their details, and writes them to a CSV file.
    It uses a memory-efficient approach by processing books one at a time.
    """
    driver = setup_driver()
    driver.get("https://library.happycoding.hk/books/")

    selectors = {
        "title": "h4.text-primary",
        "district": "i.fas.fa-map-marker",
        "author": "i.fa.fa-user",
        "copy_id": "i.fa.fa-clone",
        "publication_year": "i.fa.fa-calendar",
        "publisher": "i.fas.fa-money-bill-alt",
        "call_number": "i.fa.fa-list-ol",
        "edition": "i.fas.fa-clock",
        "new_release": "span.badge.badge-secondary.text-white"
    }

    try:
        book_elements = fetch_books(driver)
        extract_details = partial(extract_book_details, selectors)
        book_details = map(extract_details, book_elements)
        fieldnames = [
            "title", "district", "author", "copy_id",
            "publication_year", "publisher", "call_number",
            "edition", "new_release"
        ]
        count = write_books_to_csv(
            "scraped_books.csv", fieldnames, book_details)
        print(f"Total books scraped: {count}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
