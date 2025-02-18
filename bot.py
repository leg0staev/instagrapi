from methods import login_user
from instagrapi import Client
from settings import ACCOUNT_USERNAME, ACCOUNT_PASSWORD, DELAY_RANGE, PROXY

# Инициализация клиента с прокси
cl = login_user(ACCOUNT_USERNAME, ACCOUNT_PASSWORD, DELAY_RANGE, PROXY)
cl.logger.debug('залогинился')
cl.logger.debug('делаю дамп сессии')
cl.dump_settings("session.json")

cl.delay_range = [2, 5]
cl.logger.debug('выставляю задержки %s', cl.delay_range)


# Получение информации о профиле
target_username = "remont_apparatov_obn"
cl.logger.debug('цель - %s', target_username)
cl.logger.debug('получаю информацию о цели')
# user_info = cl.user_info(cl.user_id_from_username("beauty_lak_obninsk"))
user_info_dict = cl.user_info_by_username_v1(target_username).model_dump()
cl.logger.debug('информацию о цели получил')
cl.logger.debug('user_info_dict - %s', user_info_dict)

cl.logger.info(f"Username: {user_info_dict.get('username')}")
cl.logger.info(f"Followers: {user_info_dict.get('follower_count')}")
cl.logger.info(f"Following: {user_info_dict.get('following_count')}")

cl.logger.debug('получаю ID цели')
user_id = user_info_dict.get('pk')
cl.logger.debug('ID цели получил - %s', user_id)

cl.logger.debug('получаю подписчиков')
all_followers = cl.user_followers_v1(user_id, amount=0)
cl.logger.debug('подписчиков получил, сохраняю в файл')

cl.logger.debug('формирую ссылки на подписчиков')
links = {f'https://instagram.com/{user.username}/\n' for user in all_followers}
cl.logger.debug('ссылки на подписчиков формировал')
cl.logger.debug('сохраняю ссылки в файл')
with open("followers.txt", "w", encoding="utf-8") as f:
    f.writelines(links)
cl.logger.debug('список сохранил')
cl.logger.debug('работу закончил')
