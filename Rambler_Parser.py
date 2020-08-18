import requests
from bs4 import BeautifulSoup
import re


class ParsePage():

    """"
    Класс Парсера
    protocol_url_link - Переменная нужна дял корректности ссылки
    HEADERS - Заголовок , чтоб нас не завалили
    """
    protocol_url_link = 'https://m.'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    def __init__(self, url):
        # Отправляем запрос, получаем страницу
        html = self.__getting_page_html((self.protocol_url_link + url))
        # Если успешно , идем дальше
        if html.status_code == 200:
            # Получаем текст страницы
            self.parse_page = BeautifulSoup(self.__geting_html_text(html), 'html.parser')

        # Что-то иначе: логируем
        else:
            print('Ссылка недействительна')

    # Метод для получения страницы через запрос - Принимает УРЛ ссылки, без параметров
    def __getting_page_html(self, url: str, params=None):
        _getting_page = requests.get(url, headers=self.HEADERS, params=params)
        return _getting_page
    # Обработчик для получения текста html страницы
    def __geting_html_text(self, html):
        return html.text
    # Очищение от ненужной информации - получаем только цифры
    def __extracting_digits(self, text):
        return re.sub('[^0-9]', '', text)

    # Метод для получения количесива подписчиков со страницы
    def parse_page_vk_group_followers(self):
        # Ищем все элементы
        followers_items_list = self.parse_page.find_all('a', class_ = 'pm_item' , href= re.compile("act=members"))
        # Поскольку данная ссылка ведет на страницу подписчиков - из всего нам необходим любой вариант
        followers = followers_items_list[0]
        # Получаем только текст элемента
        followers_text = followers.text
        # Отчищаем от букв, переводим в инт
        return int(self.__extracting_digits(followers_text))
