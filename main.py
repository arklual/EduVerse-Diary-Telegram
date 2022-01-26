from os import EX_CANTCREAT
import aiogram
import config
from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold, hcode, hitalic, hunderline, hlink, hstrikethrough
import db_file
from parser import fill_edu_instituts
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import parser
from fsm import SignInToDiary
from aiogram.dispatcher.storage import FSMContext




#log
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token = config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# Соединение с БД
db = db_file.DBFile()

@dp.message_handler(Command('start'))
async def on_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}. Ты уже прочитал описание и знаешь, чем я могу тебе помочь.\n' 
    + 'Если вдруг ты не прочитал описание, то я твой электронный дневник, но только в телеграмме и более @хуенный. \n\n ' +
    "📍 " + hbold(' Что я могу?') + '\n'
    + '🚩 Я могу присылать тебе новые  оценки в тот момент, когда ты их получаешь.' + '\n' +
    '🚩 Также ты можешь узнать у меня' + hunderline(' оценки за определенный период времени') + ' по любому предмету.\n'
    +'🚩 И еще ты можешь смотреть ' + hunderline('итоговые оценки') + '\n' + 
    '🚩 Ты можешь вспомнить свой пароль и логин от электронного дневника' +
    '🚩 И, пока что, последняя вещь, которую я могу делать - это ' + hunderline('еженедельные отчеты.') + 
    'С их помощью ты сможешь понять что у тебя получается лучше,  а что хуже.\n\n' + '🚨' + hbold('Предупреждение') + '🚨\n' + 'Ты можешь взаимодействовать с ботом, но только после подписки.\nЧтобы подписаться нажми сюда 👉 /subscribe \n\n'
    '🆘\nСправка: /help', parse_mode='HTML'
    )

@dp.message_handler(Command('subscribe'))
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
        await message.answer(hbold('Поздравляю!!!') + '🥳😎🤓\n' + 'Ты подписался! Теперь тебе будут приходить уведомления о новых оценках', parse_mode='HTML')
    else:
        db.update_subscription(message.from_user.id, True)
        await message.answer("Ты снова подписан. Поздравляю!!!")
    


@dp.message_handler(Command('unsubscribe'))
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        await message.answer('Ты не можешь отписаться так как ты не подписывался')
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer('Ты отписался 😢😢😢 Я думаю это была случайность, поэтому вот сюда тыкай и подписывайся обратно 👉 /subscribe. У нас все только начинается, а ты уходишь. Зачем пропускать все самое интересное?🧐')
    
    

@dp.message_handler(Command('help'))
async def help_user(message: types.Message):
    await message.answer("""Вот команды, которые доступны нашему боту.\n/subscribe - подписаться на бота \n/unubscribe - отписаться от бота \n/signin_to_diary - войти в свой дневник \n/get_login - вспомнить логин от электронного дневника\n/get_password - вспомнить пароль от электронного дневника \n/get_marks - узнать о любых оценках, которые у вас стоят на данный момент \n/get_emails - получать email-рассылку о новом \n/dont_get_emails - перестать получать email-рассылку \n/leave_review - дать фидбэк и помочь нам в развитии \nЕсли что, вы всегда можете ввести '/' и ты увидишь все команды, которые ты можешь вызвать в данный момент""")


@dp.message_handler(Command('get_marks'))
async def get_marks(message: types.Message):
    pass

@dp.message_handler(Command('signin_to_diary'))
async def signin_to_diary(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        await message.answer('Прости, но ты не подписался на бота. Бот может работать только если ты на него подписан.\n Вызови /subscribe и пользуйся на здоровье')
    elif (not db.is_subscribed(message.from_user.id)):
        await message.answer('Прости, но ты не подписался на бота. Бот может работать только если ты на него подписан.\n Вызови /subscribe и пользуйся на здоровье')
    elif db.is_subscribed(message.from_user.id):
        await message.answer('Введи ' + hbold('район/город') + ' в котором ты обучаешься. \n' + hitalic('Важно: Название города или района должно совпадать с дневником!!!'), parse_mode='HTML')
        await SignInToDiary.Locality.set()

@dp.message_handler(state=SignInToDiary.Locality)
async def entered_locality_input_school(message: types.Message, state: FSMContext):
    # save answer
    locality = message.text
    """ await state.update_data(answer1 = answer) """
    await state.update_data(locality = locality) 

    await message.answer('Отлично,  двигаемся дальше.  В каком образовательном учереждении ты учишься?' + '\n' + hitalic("Важно: Название  образовательного  учереждения должно совпадать с дневником!!!"), parse_mode='HTML')
    await SignInToDiary.School.set()


@dp.message_handler(state=SignInToDiary.School)
async def entered_school_input_login(message: types.Message, state: FSMContext):
    # save answer
    school = message.text
    await state.update_data(school = school) 

    await message.answer('Отлично, двигаемся дальше. Введи логин от электронного дневника, чтобы ты мог войти в него через бота.')
    await SignInToDiary.Login.set()


@dp.message_handler(state=SignInToDiary.Login)
async def entered_login_input_password(message: types.Message, state: FSMContext):
    # save answer
    login = message.text
    await state.update_data(login = login) 

    await message.answer('Отлично, двигаемся дальше. Введи пароль от электронного дневника, чтобы ты мог войти в него через бота.')
    await SignInToDiary.Password.set()


@dp.message_handler(state=SignInToDiary.Password)
async def signup(message: types.Message, state: FSMContext):
    # save answer
    password = message.text
    await state.update_data(password = password) 

    data = await state.get_data()
    locality = data.get('locality')
    school = data.get('school')
    login = data.get('login')
    password = data.get('password')

    if parser.find_edu_instituts(locality) == False:
        #await message.answer('Не получилось получить доступ к дневнику. Попробуй еще раз. Проследи за тем, чтоб все данне совпадали с дневником. Название города/района и школы должн полностью совпадать с их названием в твоем дневнике.')
        await message.answer('В выбранном тобой городе/районе нет школ. Попробуй заново. \n\n/signin_to_diary')
    
    try:
        parser.sign_in(message.from_user.id, school, locality, login, password)
        await message.answer('Все прошло успешно. Теперь мы можем уведомлять тебя обо всех твоих оценках.')
        await state.reset_state()
    except Exception:
        await message.answer('Что-то пошло не так. Начните заново')
        await state.reset_state()



@dp.message_handler(Command('leave_review'))
async def leave_review(message: types.Message):
    # Написать статью, чтобы пользователь понял, что ему оставить в отзыве.
    await message.answer(hbold('Вы хотите оставить отзыв?') + '\n' +
    """Я очень рад, ведь фидбэк очень важен для нас, особенно сейчас, в данный промежуток времени, когда мы только начали. Но перед этим . . . \n""" +
    """Прочтите это: """ + hlink('Инструкция для фидбэка', 'https://gdz.ru/class-9/algebra/makarichev-14/569-nom/') + '\n' +
    hbold(""""'Для чего?' - спросишь ты?""")  + '\n' + """Нам важно, чтобы отзыв был 'полный'. Отзывы типа 'хорошо' или 'мне понравилось' нам нужны, но как они помогут нам развивать бота и понимать, насколько хорошо он работает? \n""" +
    hbold('Где я могу оставить отзыв?') + '\n' + """Вот здесь 👉 <a href='eduverse8@gmail.com'>eduverse8@gmail.com</a>. Также наш email можно найти в инструкции по фидбэку""" + '\n\n' + hbold('Спасибо 😊😇🙏'), parse_mode='HTML'

    )

@dp.message_handler(Command('get_emails'))
async def get_emails(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        await message.answer('Чтобы получать email-рассылку, ты должен подписаться на бота. \n Вызови команду /subcribe')
    else:
        db.update_subscription(message.from_user.id, True, True)
        await message.answer('Поздравляю!!!' + '🥳😎🤓\n' + 'Ты подписался! Теперь ты будешь осведомлен о наших новостях потому что будешь получать email-ы')

@dp.message_handler(Command('dont_get_emails'))
async def dont_get_emails(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        await message.answer('Ты и так не подписан на рассылку, а еще ты не подписан на бота. \nНадо это исправить. \nВызови команду /subcribe ')
    elif db.is_user_subcribes_bot_but_not_subcribes_email(message.from_user.id):
        await message.answer('Ты и так отписан от email-рассылки. Но я считаю, что эту ситуацию надо исправлять. \nВызови эту команду /get_email')
    else:
        db.update_subscription(message.from_user.id, True, True)
        await message.answer('Поздравляю!!!' + '🥳😎🤓\n' + 'Ты подписался! Теперь ты будешь осведомлен о наших новостях потому что будешь получать email-ы')

@dp.message_handler(Command('go_web'))
async def go_web(message: types.Message):
    pass

@dp.message_handler(Command('join_channel'))
async def join_channel(message: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)