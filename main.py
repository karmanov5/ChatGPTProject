from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import *
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pickle


def main():
    
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://poe.com/')
    driver.find_element(By.XPATH, "//button[contains(@class, 'BorderlessButton_borderlessButton')]").click()
    email = driver.find_element(By.XPATH, "//input[@type='email']")
    email.send_keys('karmanovvladislav@yandex.ru')
    email.send_keys(Keys.ENTER)
    code = input('Enter the code: ')
    placeholder = driver.find_element(By.XPATH, "//input[@placeholder='Code']")
    placeholder.send_keys(code)
    placeholder.send_keys(Keys.ENTER)
    sleep(1)
    driver.get('https://poe.com/chatgpt')
    
    textarea = driver.find_element(By.CSS_SELECTOR, 'textarea')
    wait = WebDriverWait(driver, 20)
    while True:
        text = input('Введите ваш запрос: ')
        textarea.send_keys(text)
        textarea.send_keys(Keys.ENTER)
        sleep(2)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ChatMessagesView_messageExpander')]//div[contains(@class,'ChatMessage_messageOverflowButton')]")))
        last_message = driver.find_elements(By.XPATH, "//div[contains(@class,'ChatMessage_messageRow')]")[-1]
        print(last_message.text)
        # cookies = driver.get_cookies()
        # with open('cookies.pkl', 'wb') as f:
        #     pickle.dump(cookies, f)
    sleep(1000)
    driver.quit()


if __name__ == '__main__':
    main()

