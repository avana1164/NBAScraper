from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import csv

url = "https://www.nba.com/stats/teams/advanced?Season=2024-25"

chrome_options = Options()
chrome_options.add_argument("--enable-unsafe-swiftshader")
# chrome_options.add_argument("--headless=new")  # New headless mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# setup driver and connect it to url
service = Service("../chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)
driver.implicitly_wait(20)

# for _ in range(28):
accept_cookies = driver.find_element(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")
accept_cookies.click()

dropdown = driver.find_element(By.CSS_SELECTOR, "select.DropDown_select__4pIg9")

previous_text = ""
for i in range(29, 1, -1):
    for retry in range(3):
        try:
            dropdown.click()
            driver.implicitly_wait(10)   
            season = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[3]/section[1]/div/div/div[1]/label/div/select/option[" + str(i) + "]")   
            season.click()
            dropdown.click()
            
            
            WebDriverWait(driver, 20).until(
                lambda d: previous_text != d.find_element(By.CSS_SELECTOR, "tbody.Crom_body__UYOcU").text
            )
            
            stats = driver.find_element(By.CSS_SELECTOR, "tbody.Crom_body__UYOcU")
            previous_text = stats.text
            stats_formatted = stats.text.split("\n")
            for j in range(len(stats_formatted)):
                print(stats_formatted[j])
            
            print()
            break
        except Exception as e:
            print(f"Retrying for {season.text} due to error: {e}")

driver.quit()