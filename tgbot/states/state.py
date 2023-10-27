from telebot.handler_backends import State, StatesGroup  # States


class MyStates(StatesGroup):
    start = State()
    start_func_st = State()
    get_name_st = State()
    get_age_st = State()
    payment_mont_func_st = State()
    payment_info_st = State()
    admin  =State()