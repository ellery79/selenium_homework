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

Author: Poon Ho Chuen
Date: 15 Oct 2024
Version: 1.0
"""

import csv

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


def extract_book_details(book):
    """Extract detailed information from a single book element."""
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

    details = {
        key: (
            book.find_element(By.CSS_SELECTOR, selector).text
            if key == "title"
            else extract_text(book, selector)
        )
        for key, selector in selectors.items()
        if key != "new_release"
    }

    details["new_release"] = bool(book.find_elements(
        By.CSS_SELECTOR, selectors["new_release"]))

    return details


def write_to_csv(book_details, filename="scraped_books.csv"):
    """Write a list of book detail dictionaries to a CSV file."""
    fieldnames = [
        "title", "district", "author", "copy_id",
        "publication_year", "publisher", "call_number",
        "edition", "new_release"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(book_details)

    print(f"Book details have been saved to {filename}")


def fetch_books(driver):
    """Generator to fetch all book elements across paginated pages."""
    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".card.listing-preview"))
        )
        yield from driver.find_elements(By.CSS_SELECTOR, ".card.listing-preview")

        try:
            next_button = driver.find_element(
                By.XPATH, '//a[normalize-space()="»"]')
            if next_button.is_enabled() and next_button.is_displayed():
                next_button.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
            else:
                break
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            break


def main():
    """Main function to orchestrate the scraping process."""
    driver = setup_driver()
    driver.get("https://library.happycoding.hk/books/")

    try:
        book_details = list(map(extract_book_details, fetch_books(driver)))
        list(map(print, book_details))
        write_to_csv(book_details)
        print(f"Total books scraped: {len(book_details)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
