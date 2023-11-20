from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os


TWITTER_USERNAME = os.environ['USERNAME']
TWITTER_EMAIL = os.environ['EMAIL']
TWITTER_PASSWORD = os.environ['PASSWORD']
PROMISED_DOWN = 300
PROMISED_UP = 25
INTERNET_PROVIDER = "UPC"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InternetSpeedTwitterBot:
    def __init__(self, ch_options):
        self.driver = webdriver.Chrome(options=ch_options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        accept_cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_cookie.click()
        sleep(3)
        go_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        go_button.click()
        sleep(40)
        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
        return self.down, self.up

    def tweet_at_provider(self, download, upload):
        sleep(5)
        self.driver.get("https://twitter.com/i/flow/login")
        sleep(2)
        email = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)
        sleep(2)

        try:
            password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
            password.send_keys(TWITTER_PASSWORD)
            password.send_keys(Keys.ENTER)
        except NoSuchElementException:
            authorization = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
            authorization.send_keys(TWITTER_USERNAME)
            authorization.send_keys(Keys.ENTER)
            sleep(2)
            password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
            password.send_keys(TWITTER_PASSWORD)
            password.send_keys(Keys.ENTER)

        sleep(5)
        message_input = self.driver.find_element(By.CSS_SELECTOR, 'br[data-text="true"]')
        message_input.send_keys(f"Hey {INTERNET_PROVIDER}, why is my internet speed {download}down/{upload}up when I pay for {PROMISED_UP}up/{PROMISED_DOWN}down?")
        sleep(2)
        post = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]')
        post.click()


InternetBot = InternetSpeedTwitterBot(chrome_options)
download_speed, upload_speed = InternetBot.get_internet_speed()

if float(download_speed) < PROMISED_DOWN and float(upload_speed) < PROMISED_UP:
    InternetBot.tweet_at_provider(download_speed, upload_speed)
