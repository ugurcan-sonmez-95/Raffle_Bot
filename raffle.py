from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from random import choice

class Browser:
    def __init__(self):
        self.browser = webdriver.Chrome("chromedriver_win32/chromedriver.exe")
    
    def get_html(self, url):
        self.browser.get(url)
        sleep(20) # Refresh frequency
        page_source = self.browser.page_source
        return page_source
    
    def parse_html(self, html_src):
        return BeautifulSoup(html_src, "html.parser")
    
    def close_browser(self):
        self.browser.quit()

class Raffle:
    def __init__(self):
        self.keyword = "keyword" # You can use your own keyword
        self.username = "username" # You can use your Twitch username
        self.chat_base_url = f"https://www.twitch.tv/popout/{self.username}/chat?popout="
        self.confirmed_users = set()

    def get_messages(self, soup):
        return soup.find_all("div", class_="chat-line__message")
    
    def update_confirmed_users(self, messages):
        for message in messages:
            author = message.find("span", class_="chat-author__display-name").text
            msg = message.find("span", class_="text-fragment").text
            if self.keyword in msg.lower():
                self.confirmed_users.add(author)
    
    def start_drawing(self):
        print(f"\nDrawing has started! {len(self.confirmed_users)} users have been confirmed.")
        sleep(3)
        for i in range(1, 4):
            dots = "." * i
            print("A random user is being drawn" + dots, end='\r')
            sleep(2)
        print(f"\nThe winner among {len(self.confirmed_users)} users is: {choice(list(self.confirmed_users))}")

def main():
    browser = Browser()
    raffle = Raffle()
    
    print('\n', end='')
    for _ in range(3): # Repetition count
        html_src = browser.get_html(raffle.chat_base_url)
        soup = browser.parse_html(html_src)
        messages = raffle.get_messages(soup)
        raffle.update_confirmed_users(messages)
        print(f"{len(raffle.confirmed_users)} users have been confirmed.", end='\r')
    
    raffle.start_drawing()
    browser.close_browser()

main()