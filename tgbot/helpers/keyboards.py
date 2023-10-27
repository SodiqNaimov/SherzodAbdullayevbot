from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def reply_markup(texts, row_width):
    markup = ReplyKeyboardMarkup(True, True, row_width=row_width)
    markup.add(*texts)

    return markup


def inline_markup(texts, row_width):
    markup = InlineKeyboardMarkup(row_width=row_width)
    buttons = []
    item = 0
    for i in texts:
        button = InlineKeyboardButton(i[0], callback_data='item_'+str(item+1))
        button.append(buttons)
    markup.add(*buttons)

    return markup
