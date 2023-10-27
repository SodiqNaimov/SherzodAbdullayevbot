import sqlite3
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from telebot import TeleBot
from telebot.types import Message, InputFile  # ReplyKeyboardRemove, CallbackQuery

from telebot.types import KeyboardButton
import pandas as pd
admin_panel = {}
import xlsxwriter

# for get user info
# from tgbot.helpers.user_information import User_info
from tgbot.states.state import *

# messages
from tgbot.texts.admin_messages import *

# for use keyboards
from tgbot.helpers.keyboards import *  # , inline_markup
from tgbot.texts.text_reply import *

# for use database
from tgbot.helpers.database import SQLite
from tgbot.files.config import db_path
admins = [866489508,65503218,5212887909]



def send_user(message: Message, bot: TeleBot):
    db = SQLite(db_path)
    row = db.count_of_user()
    photo = open('C:/Users/intel/PycharmProjects/Telegram bor kanal uchun/tgbot/rasm.jpg', 'rb')
    print(photo)
    caption_photo = "Telegram botimiz yangilandi!\nIltimos 👉 /start tugmasini bosing"
    for i in row:
        try:
            bot.send_photo(i[0],photo=photo,caption=caption_photo)
        except Exception as e:
            print(e)


def open_admins_panel(message: Message, bot: TeleBot):
    if message.chat.id in admins:

        bot.send_message(message.chat.id, msg_open_admins_panel, reply_markup=reply_markup(admin_btn,2))
        bot.set_state(message.from_user.id, MyStates.admin, message.chat.id)

def get_payment_data():
    db = SQLite(db_path)

    data = db.all_payment()
    # Calculate the payment statistics
    total_users = len(data)
    paid_count = sum(1 for row in data if row[0] == "Ha")
    not_paid_count = total_users - paid_count

    return paid_count, not_paid_count, total_users


def excel_of_payment(message: Message, bot: TeleBot):
    db = SQLite(db_path)
    rows = db.get_all_user_info()

    # Create a DataFrame from the query results
    df = pd.DataFrame(rows, columns=['Mijoz Ism Familyasi', 'Mijoz yoshi',"Mijoz addressi","Mijoz to'lov amalga oshirganligi haqida","To'lov amalga oshirganligining sanasi","Kurs olganligi muddati"])
    excel_file = 'info.xlsx'
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = workbook.add_worksheet('Welcome')

    # Define cell formats for header, data, and index
    header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
    data_format = workbook.add_format({'bg_color': '#FFFFFF'})
    index_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})

    # Write the header, index, and data to the worksheet
    header_row = df.columns.tolist()
    data_rows = df.values.tolist()
    worksheet.write_row(0, 1, header_row, header_format)
    for row_num, row_data in enumerate(data_rows, start=1):
        worksheet.write_row(row_num, 1, row_data, data_format)

    # Write the index column starting from 1
    index_col = df.index.tolist()
    worksheet.write_column(1, 0, [i + 1 for i in index_col], index_format)

    # Set column widths based on content
    for i, column in enumerate(df.columns, start=1):
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        worksheet.set_column(i, i, column_width)

    # Close the writer after saving
    writer.close()

    # Close the database connection

    # Send the Excel file
    with open(excel_file, 'rb') as file:
        bot.send_document(message.chat.id, file)
    open_admins_panel(message,bot)

def count_of_payment(message: Message, bot: TeleBot):
    db = SQLite(db_path)
    try:
        if len(db.payment_yes()) == 0:
            bot.send_message(message.chat.id,
                             f"👤 Foydalanuvchilar soni: <b>{len(db.count_of_user())}</b>\n\n✅ 💵 To'lov amalga oshirganlar soni: <b>0 ta</b>\n\n❎ 💵To'lov qilmaganlar soni: <b>{len(db.payment_no())}</b>")
        elif len(db.payment_no()) == 0:
            bot.send_message(message.chat.id,
                             f"👤 Foydalanuvchilar soni: <b>{len(db.count_of_user())}</b>\n\n✅ 💵 To'lov amalga oshirganlar soni: <b>{len(db.payment_yes())} ta</b>\n\n❎ 💵To'lov qilmaganlar soni: <b>0 ta</b>")
        elif len(db.payment_yes()) == 0 and len(db.payment_no()) == 0:
            bot.send_message(message.chat.id,
                             f"👤 Foydalanuvchilar soni: <b>{len(db.count_of_user())}</b>\n\n✅ 💵 To'lov amalga oshirganlar soni: <b>0 ta</b>\n\n❎ 💵To'lov qilmaganlar soni: <b>{0}</b> ta")
        else:
            bot.send_message(message.chat.id, f"👤 Foydalanuvchilar soni: <b>{len(db.count_of_user())}</b>\n\n✅ 💵 To'lov amalga oshirganlar soni: <b>{len(db.payment_yes())} ta</b>\n\n❎ 💵To'lov qilmaganlar soni: <b>{len(db.payment_no())}</b> ta")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Bazada xatolik!")
        open_admins_panel(message,bot)
    try:
        paid_count, not_paid_count, total_users = get_payment_data()

        # Calculate the payment percentages
        paid_percent = (paid_count / total_users) * 100
        not_paid_percent = (not_paid_count / total_users) * 100

        # Pie chart for percentages
        labels = ["To'lov qilganlar", "To'lov qilmaganlar"]
        sizes = [paid_percent, not_paid_percent]
        colors = ['#0077BE', '#5AB9EA']

        plt.figure(figsize=(12, 6))  # Adjust the figure size for better visualization

        # Plot the percentage pie chart
        plt.subplot(1, 2, 1)
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title("To'lov qilganlar foizlarda")

        # Plot the count pie chart
        plt.subplot(1, 2, 2)
        sizes_count = [paid_count, not_paid_count]
        colors_size = ['#00A8E8', '#80CED7']

        plt.pie(sizes_count, labels=sizes_count, colors=colors_size, startangle=140)
        plt.title("To'lov qilganlar raqamlarda")

        plt.tight_layout()  # Prevent overlapping of the two pie charts
        plt.savefig('pie_charts.png')
        plt.close()

        # Send the combined pie chart to the user
        bot.send_photo(message.chat.id, photo=open('pie_charts.png', 'rb'))
    except Exception as e:
        print(e)