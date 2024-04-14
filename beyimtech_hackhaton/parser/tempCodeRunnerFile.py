from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

def scroll_to_top(driver):
    # Прокручиваем страницу вверх на немного
    driver.execute_script("window.scrollBy(0, -5000);")

def remove_emoji(text):
    # Функция для удаления эмодзи из текста
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_ads_and_links(text):
    # Удаление URL-адресов
    text_without_urls = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Удаление текста, содержащего ссылки на сайты
    text_without_links = re.sub(r'\b(?:https?://|www\.)\S+\b', '', text_without_urls)
    
    text_without_tdotme = re.sub(r'\bt\.me/\S+\b', '', text_without_links)

    text_without_newlines = text_without_tdotme.replace('\n', '')
    return text_without_newlines



def parse_telegram_channel_selenium(channel_url, max_posts=None):
    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome()
    driver.get(channel_url)
    
    try:
        posts_parsed = 0
        while True:
            # Прокручиваем страницу вверх на немного каждые 5 секунд
            scroll_to_top(driver)
            time.sleep(5)

            # Получаем HTML-содержимое страницы
            div_elements = driver.find_elements(By.CLASS_NAME, "tgme_widget_message_text")

            for div_element in div_elements:
                # Получаем текст из элемента
                text = div_element.text
                # Удаляем эмодзи из текста
                text_without_emoji = remove_emoji(text)
                # Удаляем рекламу и ссылки из текста
                cleaned_text = remove_ads_and_links(text_without_emoji)
                # Выводим текст без эмодзи, рекламы и ссылок 
                print(cleaned_text)

                posts_parsed += 1

                # Если задано максимальное количество постов, завершаем парсинг
                if max_posts and posts_parsed >= max_posts:
                    return

    finally:
        # Важно закрывать браузер после использования
        driver.quit()

# Пример использования функции с указанием максимального количества постов (например, 30)
keywords_input = input("Введите ключевые навыки через запятую или пробел: ")
keywords = [keyword.strip().lower() for keyword in re.split(r'[,\s]+', keywords_input)]
parse_telegram_channel_selenium("https://t.me/s/jobkz_1", max_posts=30)
