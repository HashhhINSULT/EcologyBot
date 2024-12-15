import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = "8025273049:AAE-zutFbjYpKnog7GVXZ6as4w8aIUHbAzw"
bot = telebot.Telebot(TOKEN)

quiz = [
    {"question": "Предмет, который не является мусором?", "options": ["подставка для салфеток", "коробка из-под обуви", "обёртка от конфеты"], "answer": 0},
    {"question": "Куда на улицах города выбрасывают мусор?", "options": ["в мусоропровод", "на свалку", "в урну"], "answer": 2},
    {"question": "Какой мусор в природе сохранится дольше других?", "options": ["мандариновая корка", "стеклянная бутылка", "огрызок от яблока"], "answer": 1},
    {"question": "Куда нельзя выбрасывать мусор?", "options": ["в мусорный контейнер", "на свалку", "в овраг"], "answer": 2},
]

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {"current_question": 0, "score": 0}
    send_question(message.chat.id) 

def send_question(user_id):
    user = user_data[user_id]
    current = user["current_question"]

    if current < len(quiz):
        question = quiz[current]
        markup = InlineKeyboardMarkup()

for i, option in enumerate(question["options"]):
        markup.add(InlineKeyboardButton(option, callback_data=f"{current}:{i}"))
    
        bot.send_message(user_id, question["question"], reply_markup=markup)
else:
        
        score = user["score"]
        total = len(quiz)
        bot.send_message(user_id, f"Квиз завершён! Вы набрали {score} из {total}. 🎉")
        del user_data[user_id]

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = call.message.chat.id
    if user_id not in user_data:
        bot.send_message(user_id, "Нажмите /start, чтобы начать квиз.")
        return

    user = user_data[user_id]
    current = user["current_question"]
    question = quiz[current]
    correct_answer = question["answer"]
    
    question_index, user_answer = map(int, call.data.split(":"))

    if user_answer == correct_answer:
        user["score"] += 1
        bot.send_message(user_id, "Правильно! 🎉")
    else:
        bot.send_message(user_id, f"Неправильно. 😢 Правильный ответ: {question['options'][correct_answer]}")

    user["current_question"] += 1
    send_question(user_id)


@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот, который поможет тебе лучше разобраться в экологии.")



bot.polling()
