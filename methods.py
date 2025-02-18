import random
import time
from json import JSONDecodeError
from pathlib import Path

from instagrapi import Client
from instagrapi.exceptions import LoginRequired


def login_user(username, password, delay_range=None, proxy=None):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client(proxy=proxy, delay_range=delay_range)

    try:
        session = cl.load_settings(Path("session.json"))
    except JSONDecodeError:
        cl.logger.info("Не смог спарсить данные сессии")
        session = None

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(username, password)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                cl.logger.info("Сессия не валидна, нужно логиниться через юсернэйм и пароль")
                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                cl.login(username, password)
            login_via_session = True
        except Exception as e:
            cl.logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            cl.logger.info(
                "Попытка войти в систему с помощью имени пользователя и пароля. имя пользователя: %s" % username)
            if cl.login(username, password):
                login_via_pw = True
        except Exception as e:
            cl.logger.info("Не удалось войти в систему с помощью имени пользователя и пароля: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Не удалось войти в систему ни с помощью пароля, ни с помощью сесии")
    return cl


def save_to_file(data, filename):
    """
    Функция для сохранения данных в текстовый файл.
    """
    with open(filename, 'a', encoding='utf-8') as file:  # Открываем файл в режиме дополнения
        file.writelines(str(data) + '\n')  # Записываем данные в файл


def random_sleep(
        simple_sleep_time: tuple[int],
        big_sleep_time: tuple[int],
        cycles_count: tuple[int],
        current_count: int
) -> None:
    """Устанавливает время сна в зависимости от номера текущего цикла"""
    count = random.randint(*cycles_count)
    if count == current_count:
        time.sleep(random.randint(*big_sleep_time))
    else:
        time.sleep(random.randint(*simple_sleep_time))
