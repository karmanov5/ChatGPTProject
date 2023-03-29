# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from time import sleep
from os import environ
from dotenv import load_dotenv
import pickle, vk_api, random, re, requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from io import BytesIO
from PIL import Image
import json

load_dotenv()

api_key_vk = environ.get('API_KEY_VK')

vk_session = vk_api.VkApi(token=api_key_vk)
vk = vk_session.get_api()
s = Service(executable_path='geckodriver.exe')


def send_message(name, message_id, chat_id, message):
    vk.messages.send(
        # peer_id=chat_id,
        chat_id=chat_id,
        message=f'{name}, {message[0].lower() + message[1:]}',
        # forward_messages=message_id,
        random_id=random.randint(1, 1000)
    )



def get_name(uid: int):
    return f"@id{uid}"



def main():
    
    options = webdriver.FirefoxOptions()
    options.headless = False
    # options.binary_location
    options.binary_location=r"C:\Program Files\Mozilla Firefox\firefox.exe"
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Firefox(service=s, options=options)
    driver.get('https://poe.com/')
    driver.find_element(By.XPATH, "//button/div[text()[contains(.,'Use email')]]").click()
    email = driver.find_element(By.XPATH, "//input[@type='email']")
    email.send_keys('karmanovvladislav@yandex.ru')
    email.send_keys(Keys.ENTER)
    code = input('Enter the code: ')
    placeholder = driver.find_element(By.XPATH, "//input[@placeholder='Code']")
    placeholder.send_keys(code)
    placeholder.send_keys(Keys.ENTER)
    sleep(1)
    driver.get('https://poe.com/chatgpt')
    print('Зашел на сайт!')
    textarea = driver.find_element(By.CSS_SELECTOR, 'textarea')
    wait = WebDriverWait(driver, 120)
    while True:

        longpool = VkBotLongPoll(vk_session, 219298440)
        try:
            for event in longpool.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    
                    message_text = event.message['text']
                    attachments = event.message['attachments'][0] if len(event.message['attachments']) > 0 else []
                    message_id = event.message['conversation_message_id']
                    user_id = event.message['from_id']
                    chat_id = event.chat_id
                   
                    promt = re.search(r'[Аа]нтон[\S]*[\s]*(?P<promt>[\w\s\S]*)', message_text)
                    promt = '' if promt is None else promt.group('promt')
                    print('User:', user_id, 'Message:', promt)
                    if f'[club{event.group_id}|Умный бот Антон]' in message_text:
                        image = re.search(r'[Нн]арисуй\s*(?P<image>[\w\s\S]*)', promt)
                        edit_image = re.search(r'[Ии]змени\s*[фотографияюкартинкау]*', promt)
                        if edit_image is not None and len(attachments) > 0 and attachments['type'] == 'photo':
                            # image_url = attachments['photo']['sizes'][-1]['url']
                            # image_source = requests.get(image_url)
                            # with open('image.png', 'wb') as f:
                            #     f.write(image_source.content)
                            
                            # image = Image.open('image.png')
                            # image = image.resize((256, 256))

                            # byte_stream = BytesIO()
                            # image.save(byte_stream, format='PNG')
                            # byte_array = byte_stream.getvalue()
                            # completion = openai.Image.create_variation(
                            #         image=byte_array,
                            #         n=1,
                            #         size='1024x1024'
                            #     )
                            # image_url = completion['data'][0]['url']
                            # filename = 'image.png'
                            # response = requests.get(image_url)
                            # with open(filename, 'wb') as f:
                            #     f.write(response.content)
                            completion_text = 'К сожалению, я пока не могу обработать и нарисовать ваши фотографии :('
                            # print('Ответ бота:', completion_text)
                            send_message(name=get_name(user_id), message_id=message_id, chat_id=chat_id, message=completion_text)

                        elif image is not None:
                            # image = image.group('image')
                            # completion = openai.Image.create(
                            #     prompt=image,
                            #     n=1,
                            #     size='1024x1024'
                            # )
                            # image_url = completion['data'][0]['url']
                            # filename = 'image.png'
                            # response = requests.get(image_url)
                            # with open(filename, 'wb') as f:
                            #     f.write(response.content)
                            completion_text = 'К сожалению, я пока не могу обработать и нарисовать ваши фотографии :('
                            # print('Ответ бота:', completion_text)
                            send_message(name=get_name(user_id), message_id=message_id, chat_id=chat_id, message=completion_text)
                        else:   
                            # completion = openai.Completion.create(
                            #             engine=engine,
                            #             prompt=promt,
                            #             temperature=0.5,
                            #             max_tokens=1000
                            #         )
                            # completion_text = completion.choices[0]['text']
                            # text = input('Введите ваш запрос: ')
                            textarea.send_keys(promt)
                            textarea.send_keys(Keys.ENTER)
                            sleep(3)
                            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ChatMessagesView_messageExpander')]//div[contains(@class,'ChatMessage_messageOverflowButton')]")))
                            last_message = driver.find_elements(By.XPATH, "//div[contains(@class,'ChatMessage_messageRow')]")[-1]
                            # print(last_message.text)
                            print('Ответ бота:', last_message.text)
                            send_message(get_name(user_id), message_id, chat_id, last_message.text)

        except Exception as ex:
            print('Ошибка:', ex)

    while True:
        text = input('Введите свое сообщение: ')    
        textarea.send_keys(text)
        textarea.send_keys(Keys.ENTER)
        sleep(3)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ChatMessagesView_messageExpander')]//div[contains(@class,'ChatMessage_messageOverflowButton')]")))
        last_message = driver.find_elements(By.XPATH, "//div[contains(@class,'ChatMessage_messageRow')]")[-1]
        print(last_message.text)

if __name__ == '__main__':
    main()

