import time

from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, ChatJoinRequest, ReplyKeyboardRemove

# for get user info
from tgbot.helpers.user_information import User_info
from datetime import datetime, timedelta

# for state
from tgbot.states.state import MyStates

# messages
from tgbot.texts.messages import *

# for use keyboards
from tgbot.helpers.keyboards import reply_markup  # , inline_markup
from tgbot.texts.text_reply import *

# for use database
from tgbot.helpers.database import SQLite
from tgbot.files.config import db_path

user_data = {}


def start(message: Message, bot: TeleBot):
    user = User_info(message)
    user_data[message.chat.id] = {'get_name': '', 'get_age': '', 'get_region': '', 'payment_month': ''}
    db = SQLite(db_path)
    is_register = db.is_registered(message.chat.id)
    if len(is_register) == 0:
        bot.send_message(user.chat_id, msg_start)
        start_func(message, bot)
    else:
        payment_mont_func(message, bot)


def start_func(message: Message, bot: TeleBot):
    user = User_info(message)
    time.sleep(0.7)
    bot.send_message(user.chat_id, get_name_message)
    bot.set_state(message.from_user.id, MyStates.start_func_st, message.chat.id)


def get_name_func(message: Message, bot: TeleBot):
    user = User_info(message)
    user_data[message.chat.id]['get_name'] = message.text
    bot.send_message(user.chat_id, get_age_message)
    bot.set_state(message.from_user.id, MyStates.get_name_st, message.chat.id)


def get_age(message: Message, bot: TeleBot):
    user = User_info(message)
    age = message.text
    try:
        n = int(message.text)
    except Exception as e:
        bot.send_message(message.chat.id, get_age_error_message)
        bot.set_state(message.from_user.id, MyStates.get_name_st, message.chat.id)
    else:
        if len(age) != 2:
            bot.send_message(message.chat.id, get_age_count_message)
            bot.set_state(message.from_user.id, MyStates.get_name_st, message.chat.id)
        else:
            user_data[message.chat.id]['get_age'] = message.text
            bot.send_message(user.chat_id, get_region_message, reply_markup=reply_markup(region_btn, 2))
            bot.set_state(message.from_user.id, MyStates.get_age_st, message.chat.id)


def get_region(message: Message, bot: TeleBot):
    user_data[message.chat.id]['get_region'] = message.text
    # Get the current date and time
    current_date_time = datetime.now()
    # Extract only the date part from the datetime object
    # current_date = current_date_time.date()current_date
    db = SQLite(db_path)
    db.register_user(message.chat.id, user_data[message.chat.id]['get_name'], user_data[message.chat.id]['get_age'],
                     user_data[message.chat.id]['get_region'], "Yo'q")
    payment_mont_func(message, bot)


def payment_mont_func(message: Message, bot: TeleBot):
    user = User_info(message)
    bot.send_message(user.chat_id, kurs_info)
    bot.send_message(user.chat_id, payment_mont, reply_markup=reply_markup(payment_month_btn, 3))
    bot.set_state(message.from_user.id, MyStates.payment_mont_func_st, message.chat.id)


def payment_info(message: Message, bot: TeleBot):
    user = User_info(message)
    user_data[message.chat.id]['payment_month'] = message.text
    bot.send_message(user.chat_id, payment_about, reply_markup=reply_markup(["⬅️ Ortga"], 1))
    bot.send_message(user.chat_id, payment_card)
    bot.set_state(message.from_user.id, MyStates.payment_info_st, message.chat.id)


def back_payment_info(message: Message, bot: TeleBot):
    payment_mont_func(message, bot)


def send_group_payment_check(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, wait_confirmation_message)
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    db = SQLite(db_path)
    data = db.get_user_info(message.chat.id)
    img = open("image.jpg", 'rb')
    inline_keyboard = InlineKeyboardMarkup(row_width=2)

    inline_keyboard.add(InlineKeyboardButton("✅ Tasdqilash", callback_data=str(message.chat.id) + "_tasdiqlash"),
                        InlineKeyboardButton("❌ Rad etish", callback_data=str(message.chat.id) + "_cancel"))
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    silka = message.from_user.username
    if message.from_user.username is None:
        msg = f"Yangi to'lov!\n\n👤 Mijoz: {data[0]}\n🧾 Mijoz yoshi: {data[1]}\n📭 *Telegram account*: {mention}\n📍 Yashash Joyi: {data[2]} \n🕦 Kurs davomiyligi{user_data[message.chat.id]['payment_month']} "
        bot.send_photo(-1001985025212, img, caption=msg, reply_markup=inline_keyboard, parse_mode="Markdown")

    else:
        msg = "Yangi to'lov!\n\n" + "👤 Mijoz: " + str(data[0]) + '\n' + "🧾 Mijoz yoshi: " + str(
            data[1]) + "\n📭 <b>Telegram account: @</b>" + silka + "\n📍 Yashash Joyi: " + data[
                  2] + '\n' + "🕦 Kurs davomiyligi: " + user_data[message.chat.id]['payment_month']
        bot.send_photo(-1001985025212, img, caption=msg, reply_markup=inline_keyboard)

    #-998165381 Kanal opsujdeniy
def cachel(call: CallbackQuery, bot: TeleBot):
    # print(call.data.split("_")[0])
    chat_id = call.data.split("_")[0]

    bot.edit_message_caption(call.message.caption + "\n\n<b>❌ Rad etildi</b>", call.message.chat.id,
                             call.message.message_id)
    bot.send_message(chat_id, f"Sizning to'lovingiz qabul qilinmadi.")


def tasdiq(call: CallbackQuery, bot: TeleBot):

    db = SQLite(db_path)
    chat_id = call.data.split("_")[0]
    current_date_time = datetime.now()
    current_date = current_date_time.date()
    payment_month = int(user_data[int(chat_id)]['payment_month'].split(" ")[0])
    # print(payment_month)
    if payment_month == 1:
        days = 30
    elif payment_month == 3:
        days = 90
    else:
        days = 150
    print(db.get_user_pay(chat_id))
    if db.get_user_pay(chat_id):
        end_time = current_date + timedelta(days=days + 1)
    else:
        end_time = current_date + timedelta(days=days)

    # print(end_time)
    db.update_user_payment(chat_id, "Ha", current_date, end_time)
    # print(call.message.text)
    bot.edit_message_caption(call.message.caption + "\n\n<b>✅ Qabul qilindi</b>", call.message.chat.id,
                             call.message.message_id)

    link = bot.create_chat_invite_link(chat_id=-1001978553409, name=call.message.text, creates_join_request=True).invite_link
    group_link = bot.create_chat_invite_link(chat_id=-1001952801511, name=call.message.text).invite_link

    # print(link)
    bot.send_message(chat_id, f"Sizning to'lovingiz qabul qilindi, mana sizning gruppa uchun ssilkangiz \n\n{group_link}",protect_content=True)
    bot.send_message(chat_id, f"Sizning to'lovingiz qabul qilindi, mana sizning kanal uchun ssilkangiz \n\n{link}",protect_content=True)

    # except Exception as e:
    #     bot.send_message(866489508, e)


def approve(update: ChatJoinRequest, bot: TeleBot):
    db = SQLite(db_path)

    for i in db.get_pay_users():
        if i[0] == update.from_user.id:
            bot.approve_chat_join_request(update.chat.id, update.from_user.id)
def check_from_group(message: Message, bot: TeleBot):
    print('s')
    db = SQLite(db_path)
    chat_id = -1001952801511
    for new_member in message.new_chat_members:
        user_id = new_member.id
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_member.status == "member":
            # Check if the user is in the allowed list
            if user_id not in [i[0] for i in db.get_pay_users()]:
                bot.kick_chat_member(chat_id, user_id)
                time.sleep(7)
                bot.unban_chat_member(chat_id, user_id)