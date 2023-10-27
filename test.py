# user = []
# name = input("Salom Ismingizni kiriting: ")
# user.append(name)
# family_name = input("Familyangizni kiriting: ")
# user.append(family_name)
# age = input("Yoshingizni kiriting kiriting: ")
# user.append(age)
# # for i in user:
# #     print(i)
# print(f"Mijozning ismi: {user[0]} \nMijozning Familyasi: {user[1]} \nMijozning yoshi: {user[2]} yoshda")
import time

import telebot
from tgbot.files.config import *
from tgbot.helpers.database import *
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6320104108:AAFiFxOmvll7Xhdj2SAzRyZOq_7SUr57Aew')

# Replace 'YOUR_SUPERGROUP_CHAT_ID' with the actual chat ID of your supergroup
supergroup_chat_id = '-1001959374778'

@bot.message_handler(commands=['create_link'])
def create_link(message):
    try:
        bot.unban_chat_member(-1001959374778, 5212887909)

        invite_link = bot.create_chat_invite_link(supergroup_chat_id)
        bot.reply_to(message, f"Here's the invite link for the supergroup: {invite_link.invite_link}")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")
@bot.message_handler(content_types=['new_chat_members'])
def check_from_group(message):
    db = SQLite(db_path)
    chat_id = -1001959374778
    for new_member in message.new_chat_members:
        user_id = new_member.id
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_member.status == "member":
            # Check if the user is in the allowed list
            if user_id not in [i[0] for i in db.get_pay_users()]:
                bot.kick_chat_member(chat_id, user_id)
                time.sleep(7)
                bot.unban_chat_member(chat_id, user_id)
    # db = SQLite(db_path)
    # for new_member in message.new_chat_members:
    #     user_id = new_member.id
    #     for i in db.get_pay_users():
    #         if i[0] == user_id:
    #             print('yes')
    #         elif user_id != i[0]:
    #             bot.kick_chat_member(-1001959374778, i)
    #             bot.unban_chat_member(-1001959374778, i)
    # #         # bot.approve_chat_join_request(update.chat.id, update.from_user.id)
    #

# bot.polling()
# myTuple = ([1, 2], [3])
# myTuple[1].append(4)
# print(myTuple)
a = 15.0

if a.is_integer():
    print("Bu o'zgaruvchi int tipida")
else:
    print("Bu o'zgaruvchi int tipida emas")
