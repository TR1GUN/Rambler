from Rambler_DataBase import DataBase
from Rambler_Parser import ParsePage
import Rambler_Const
import os
import datetime
import time

# Когда все в сборе можно начинать


class Program():
    """
    Класс Основной программы

    """
    DataBase = DataBase()
    #
    site_page_list = Rambler_Const.site_page_list

    def __init__(self):
        # Для начала - зальем в нашу базу данных те группы, которые есть в константах
        self.__checking_database_with_constants()
        # Теперь запускаем парсер
        self.parse_and_save_count_followers_vk_group()

    # Заливка в базу данных групп из констант
    def __checking_database_with_constants(self):
        for i in range(len(self.site_page_list)-1):
            self.DataBase.data_base_adding_new_group_to_database(self.site_page_list[i])

    # Получаем количество подписоты группы в контакте
    def __parse_vk_group_count_followers(self, link:str):

        parse = ParsePage(link)
        count_followers = parse.parse_page_vk_group_followers()
        return count_followers

    # Получаем дату - Строка
    def __get_date(self):
        date = str(datetime.datetime.now())
        return str(date[:10])

    # Метод для сохранения в базу данных
    def __save_to_database_vk_group_information_about_followers(self, link_group: str, followers: int):
        self.DataBase.database_adding_information_about_followers(link_group=link_group, followers=followers, date=self.__get_date())

    # Метод для Парсинга и сохранения в базу данных
    def parse_and_save_count_followers_vk_group(self):
        # Получаем список групп
        list_group = self.DataBase.database_get_list_all_link_group()
        for i in range(len(list_group)-1):
        # Проходимся по каждой из них
            count_followers = self.__parse_vk_group_count_followers(list_group[i])
        # Сохраняем
            self.__save_to_database_vk_group_information_about_followers(link_group= list_group[i], followers = count_followers)
            time.sleep(10)







