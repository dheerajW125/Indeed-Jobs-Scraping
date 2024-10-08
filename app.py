from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

import pandas as pd

# List to store job data
job_data = []

# Set up Chrome options to spoof the user-agent
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Provide the path to chromedriver
service = Service(r'C:\Users\dheer\Downloads\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# Open the Indeed job listing URL
url = 'https://in.indeed.com/jobs?q=Python&l=India&from=searchOnDesktopSerp&vjk=bf174b8d63e5fe59'
driver.get(url)

# Set page limit
page_limit = 3
current_page = 1

while current_page <= page_limit:
    cards = driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon')  # Update cards before checking
    if cards:
        for card in cards:
            try:
                job_title = card.find_element(By.CSS_SELECTOR, 'span[id^="jobTitle-"]').text.strip()
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

            # Store the data in the list as a dictionary
            job_data.append({
                'Job Title': job_title,
                'Company': company,
                'Location': location,
                'Job Summary': job_summary,
                'Salary Range': salary,
                'Posted Date': posted_date,
                'Today': today,
                'Job Link': job_url
            })

        # Try to find the "Next Page" button and go to the next page
        try:
            next_page = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(next_page).perform()
            next_page.click()  # Click the "Next Page" button
            time.sleep(4)  # Wait for the next page to load
            current_page += 1  # Move to the next page
        except NoSuchElementException:
            print("No more pages to scrape.")
            break  # Exit if the next page button doesn't exist
    else:
        print("No job cards found.")
        break

driver.quit()

# Create a DataFrame from the job_data list
df = pd.DataFrame(job_data)

# Save the DataFrame to an Excel file
df.to_excel('indeed_jobs2.xlsx', index=False)

print("Job data has been saved to 'indeed_jobs.xlsx'.")
