import sqlite3 as lite
import sqlite3
import os

class DataBase():
    """
    Класс для работы с Базами данных
    """
    name_data_base = 'Rambler_DataBase.db'
    def __init__(self):

        # Создаем базу данных
        user_data_base = sqlite3.connect(self.name_data_base)
        data_base = user_data_base.cursor()
        # Создаем первую базу данных - Линк группы , Ид - уникальный Номер группы
        data_base.execute("CREATE TABLE IF NOT EXISTS \"Groups_VK\" (\"link_group\" TEXT, \"ID\" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)")
        #Создаем вторую базу данных - Ид, время , количество подписоты
        data_base.execute("CREATE TABLE IF NOT EXISTS \"Groups_VK_followers_by_date\" ( \"ID\" INTEGER, \"date\" TEXT, \"followers_count\" INTEGER)")
        # # Создаем базу данных - поля таблицы: ник пользователя , пароль , Куки
        data_base.close()

    # Коннект с БД
    def __database_connect(self):
        user_data_base = sqlite3.connect(self.name_data_base)
        data_base = user_data_base.cursor()
        return data_base

    # Отправляем линк группы в базу данных
    def data_base_adding_new_group_to_database(self, link_group):
        # Проверяем на дубликацию значений :
        self.duplicate = self.__database_check_duplicate_link_group(link_group)
        if self.duplicate == False:
            user_data_base = sqlite3.connect(self.name_data_base)
            data_base = user_data_base.cursor()
            data_base.execute("INSERT INTO \"Groups_VK\"(\"link_group\") VALUES (?)", (link_group,))
            user_data_base.commit()
            data_base.close()
        # Иначе - логируем
        else:
            print("Такая группа существует")

    # Чтоб не выстрелить себе в ногу - сделаем проверку на дубликат групп.
    def __database_check_duplicate_link_group(self, link_group):
        user_data_base = sqlite3.connect(self.name_data_base)
        data_base = user_data_base.cursor()
        data_base.execute('SELECT \"link_group\" FROM \"Groups_VK\"  WHERE \"link_group\" = (?)', (link_group,))
        data = data_base.fetchall()
        data_base.close()
        # проверяем на пустоту:
        if not data:
            return False
        else:
            return True

    # Поиск Максимального Значения ид
    def __database_find_max_value_to_id(self):
        user_data_base = sqlite3.connect(self.name_data_base)
        data_base = user_data_base.cursor()
        data_base.execute('SELECT MAX(ID) FROM Groups_VK')
        data = data_base.fetchone()[0]
        data_base.close()
        if data is int:
            return data
        else:
            return 0

    # Получение id по названию группы
    def __database_get_id_by_group_name(self, link_group):
        data_base = self.__database_connect()
        data_base.execute('SELECT \"ID\" FROM \"Groups_VK\"  WHERE \"link_group\" = (?)', (link_group,))
        data = data_base.fetchone()[0]
        print(data, type(data))
        data_base.close()
        return data

    # Запись в бд полученной информации
    def database_adding_information_about_followers(self, link_group:str, followers:int, date:str):
        # Получаем ид по названию группы
        id = self.__database_get_id_by_group_name(link_group)
        user_data_base = sqlite3.connect(self.name_data_base)
        data_base = user_data_base.cursor()
        data_base.execute("INSERT INTO \"Groups_VK_followers_by_date\"(\"ID\", \"date\",\"followers_count\" ) VALUES (?, ? , ?)", (id, date, followers,))
        user_data_base.commit()
        data_base.close()

    # Получаем линки групп
    def database_get_list_all_link_group(self):
        data_base = self.__database_connect()
        data_base.execute('SELECT \"link_group\" FROM \"Groups_VK\"')
        data = data_base.fetchall()
        data_base.close()
        data = self.__normalization_from_data_group_to_list(data)
        print(data)
        return data

    # Нормализуем данные групп - Ето важно!
    def __normalization_from_data_group_to_list(self, data):
        group_list = []
        for i in range(len(data)-1):
            group_list.append(data[i][0])
        return group_list



