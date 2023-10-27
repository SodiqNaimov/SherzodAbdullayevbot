import datetime

import schedule
import time
import threading

import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from tgbot.files.config import token
from tgbot.handlers.user import *
from tgbot.handlers.admin import *

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage, num_threads=5, parse_mode='HTML')


def check_database():
    try:
        db = SQLite(db_path)
        users = db.check_term()
        current_date = datetime.now()
        day_1 = []
        kick = []

        for i in users:
            if i[1] == str(current_date.date()):
                day_1.append(i[0])
            elif datetime.strptime(i[1], '%Y-%m-%d') + timedelta(days=1) < current_date:
                kick.append(i[0])
                print(kick)

        print(day_1)
        print(kick)

        for i in day_1:
            bot.send_message(i, "To'lov muddati tugab bormoqda. Ertagacha to'lov qilmasangiz, "
                                "kanaldan va gruppadan chiqarib yuboramiz. /start")

        for i in kick:
            db.update_user_not_payment(i)
            print('f')
            # print(day_1)
            # print(kick)
            bot.kick_chat_member(-1001978553409, i)
            bot.unban_chat_member(-1001978553409, i)
            print(i)
            bot.kick_chat_member(-1001952801511, i)
            bot.unban_chat_member(-1001952801511, i)
            print(i)
            bot.send_message(i, "Siz kanaldan va gruppadan chiqarib yuborildingiz!")
    except Exception as e:
        bot.send_message(866489508, e)


# check_database()
# Schedule the function to run every day at a specific time
# schedule.every().day.at("19:00").do(check_database)
# s = schedule.every().day.at("08:00").do(check_database)
s = schedule.every().second.do(check_database)




def register_m_handler(func, text, state, commands):
    return bot.register_message_handler(func, text=text, state=state, commands=commands, pass_bot=True)


region_filter = ['Andijon viloyati', 'Buxoro viloyati', 'Fargʻona viloyati', 'Jizzax viloyati', 'Xorazm viloyati', 'Namangan viloyati',
                 'Qashqadaryo viloyati', 'Navoiy viloyati', 'Qoraqalpogʻiston Respublikasi', 'Samarqand viloyati', 'Sirdaryo viloyati',
                 'Surxondaryo viloyati', 'Toshkent viloyati']


def register_handlers():
    bot.register_message_handler(start, commands=['start'], pass_bot=True)

    bot.register_message_handler(check_from_group, content_types=['new_chat_members'], pass_bot=True)

    bot.register_callback_query_handler(tasdiq, func=lambda call: call.data.endswith("_tasdiqlash"), pass_bot=True)
    bot.register_callback_query_handler(cachel, func=lambda call: call.data.endswith("_cancel"), pass_bot=True)

    register_m_handler(start_func, None, MyStates.start, None)

    register_m_handler(get_name_func, None, MyStates.start_func_st, None)

    register_m_handler(get_age, None, MyStates.get_name_st, None)

    register_m_handler(get_region, region_filter, MyStates.get_age_st, None)
    register_m_handler(back_payment_info, "⬅️ Ortga", MyStates.payment_info_st, None)

    register_m_handler(payment_info, ["1 oy - 200.000 so'm", "3 oy - 500.000 so'm", "5 oy - 800.000 so'm"], MyStates.payment_mont_func_st, None)

    bot.register_message_handler(send_group_payment_check, state=MyStates.payment_info_st, content_types=['photo'], pass_bot=True)

    bot.register_chat_join_request_handler(approve,  pass_bot=True)

    #  ADMIN
    bot.register_message_handler(open_admins_panel, commands=['admin'], pass_bot=True)
    bot.register_message_handler(send_user, commands=['send'], pass_bot=True)

    register_m_handler(count_of_payment, "👤 Foydalanuvchilar ma'lumoti text", MyStates.admin, None)
    register_m_handler(excel_of_payment, "👤 Foydalanuvchilar haqida ma'lumot excel", MyStates.admin, None)


def run():
    bot.infinity_polling(skip_pending=True)


register_handlers()

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.IsDigitFilter())


def schedul():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=schedul)
bot_polling_thread = threading.Thread(target=run)

# Start both threads
schedule_thread.start()
bot_polling_thread.start()
