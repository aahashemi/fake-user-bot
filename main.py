import requests
from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, \
    MessageHandler, Filters, PreCheckoutQueryHandler, ShippingQueryHandler
import logging
import os
import random

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
Admin_Chat_ID = 875163639

MALE = 'Male ♂'
FEMALE = 'Female ♀'
RANDOM = 'Random ♂♀'
DONATE = 'Donate ☕️'

Button = [[RANDOM], [MALE, FEMALE], [DONATE]]
ButtonPack = ReplyKeyboardMarkup(Button, resize_keyboard=True)

buyMeCoffee = [[InlineKeyboardButton('Buy me a coffee ☕️', callback_data='donate', url='https://www.buymeacoffee.com/aahashemi')]]
buyMeCoffeePack = InlineKeyboardMarkup(buyMeCoffee)
# ----------------------------------------------------------------------------------------

def generate_fake_user(gender=None):
    url = "https://fake-users6.p.rapidapi.com/"
    querystring = {"gender": gender}
    headers = {
        'x-rapidapi-host': "fake-users6.p.rapidapi.com",
        'x-rapidapi-key': "f46d0d682dmsh95ed9f4dc7225e2p146570jsn1d8f86b7de46"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_response = response.json()

    gender = json_response['results'][0]['gender']
    first_name = json_response['results'][0]['name']['first']
    last_name = json_response['results'][0]['name']['last']
    full_name = first_name + ' ' + last_name
    street_number = json_response['results'][0]['location']['street']['number']
    street_name = json_response['results'][0]['location']['street']['name']
    city = json_response['results'][0]['location']['city']
    state = json_response['results'][0]['location']['state']
    country = json_response['results'][0]['location']['country']
    postcode = json_response['results'][0]['location']['postcode']
    # timezone = json_response['results'][0]['location']['timezone']['description']
    age = json_response['results'][0]['dob']['age']
    mobile_phone = json_response['results'][0]['cell']
    phone = json_response['results'][0]['phone']
    email = json_response['results'][0]['email']
    photo = json_response['results'][0]['picture']['large']

    message = f'Gender: {gender}\n' \
              f'Age: {age}\n' \
              f'Full name: {full_name}\n\n' \
              f'Address: {street_number}, {street_name}, {city}, {state}, {country}\n' \
              f'Postal code: {postcode}\n\n' \
              f'Email: {email}\n' \
              f'Mobile phone: {mobile_phone}\n' \
              f'Phone: {phone}\n\n' \
              f'by @FakeUserGenerator_bot 🤖'

    return (message, photo)



def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Welcome to Fake User Generator!',
                              reply_markup=ButtonPack)

    context.bot.send_message(chat_id=Admin_Chat_ID,
                             text=f'✅ @{update.effective_user.username} started the bot!')

def edit_message_text(context, chat_id, message_id,text):
    context.bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text)

def TextHandler(update: Update, context: CallbackContext) -> None:
    text = str(update.message.text)

    context.bot.send_chat_action(
        chat_id=update.effective_user.id,
        action='typing'
    )

    if text == RANDOM:
        fake_user = generate_fake_user()
        context.bot.send_photo(
            chat_id=update.effective_user.id,
            caption=fake_user[0],
            photo=fake_user[1]
        )

    elif text == MALE:
        fake_user = generate_fake_user('male')
        context.bot.send_photo(
            chat_id=update.effective_user.id,
            caption=fake_user[0],
            photo=fake_user[1]
        )

    elif text == FEMALE:
        fake_user = generate_fake_user('female')
        context.bot.send_photo(
            chat_id=update.effective_user.id,
            caption=fake_user[0],
            photo=fake_user[1]
        )

    elif text == DONATE:
        color_list = ['black', 'blue', 'green', 'orange', 'red', 'violet', 'white', 'yellow']
        color = (random.choice(color_list))
        txt = ''
        update.message.reply_photo(
            photo=open(f"{color}.png", "rb"),
            caption=txt,
            reply_markup=buyMeCoffeePack
        )
        context.bot.send_message(chat_id=Admin_Chat_ID,
                                 text=f'☕ @{update.effective_user.username} might donate!')


def main():
    TOKEN = "5179969659:AAFQn7vHTXl2554p4n-_cHiZey51SagAGnI"
    APP_NAME = 'https://fake-user.herokuapp.com/'

    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, TextHandler, run_async=True))

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
