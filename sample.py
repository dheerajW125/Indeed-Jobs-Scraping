import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Set up Chrome options to spoof the user-agent
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Provide the path to chromedriver
service = Service(r'C:\Users\dheer\Downloads\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# Open the Indeed job listing URL
url = 'https://in.indeed.com/jobs?q=Python&l=India&from=searchOnDesktopSerp&vjk=bf174b8d63e5fe59'
driver.get(url)

# Initialize an empty list to store job data
all_jobs = []

while True:
    # Check if there are any job cards found
    cards = driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon')
    if cards:
        for card in cards:
            try:
                atag = card.find_element(By.TAG_NAME, 'a')
                job_title = atag.get_attribute('title')
            except:
                job_title = "N/A"

            try:
                company = card.find_element(By.CSS_SELECTOR, 'div.css-1qv0295 > span[data-testid="company-name"]').text.strip()
            except:
                company = "N/A"

            try:
                location = card.find_element(By.CSS_SELECTOR, 'div[data-testid="text-location"]').text.strip()
            except:
                location = "N/A"

            try:
                job_summary = card.find_element(By.CSS_SELECTOR, 'div.css-9446fg').text.strip()
            except:
                job_summary = "N/A"

            try:
                posted_date_element = card.find_element(By.CSS_SELECTOR, 'span[data-testid="myJobsStateDate"]').text.strip()
                posted_date = posted_date_element.split("Just posted")[-1].strip() if "Just posted" in posted_date_element else posted_date_element
            except:
                posted_date = "N/A"

            try:
                salary = card.find_element(By.CSS_SELECTOR, 'div[data-testid="attribute_snippet_testid"]').text.strip()
            except:
                salary = "N/A"

            try:
                atag = card.find_element(By.CSS_SELECTOR, 'a[data-jk]')
                job_url = 'https://www.indeed.com' + atag.get_attribute('href')
            except:
                job_url = "N/A"

            today = datetime.today().strftime('%d-%m-%Y')

            # Add the extracted job details to the list
            all_jobs.append((job_title, company, location, posted_date, today, job_summary, salary, job_url))

        # Try to find the "Next Page" button and go to the next page
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
            next_page.click()  # Click the "Next Page" button
            time.sleep(2)  # Wait for the next page to load
        except NoSuchElementException:
            print("No more pages to scrape.")
            break  # Exit if the next page button doesn't exist
    else:
        print("No job cards found.")
        break

driver.quit()

# Convert the job data to a DataFrame and save it as an Excel file
columns = ['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary', 'JobUrl']
df = pd.DataFrame(all_jobs, columns=columns)
df.to_excel('indeed_job_listings.xlsx', index=False)
print("Job data has been saved to indeed_job_listings.xlsx")
