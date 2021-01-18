from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World! This is a webhook created using heroku to use the twilio api for creating a wattsapp bot."


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'hi' in incoming_msg or 'hey' in incoming_msg or 'hello' in incoming_msg or 'menu' in incoming_msg:
        text = f'Hello !!! 🙋🏽‍♂ \n \nThis is a Wattsapp-Bot developed by Aryan Nath (aryannath.github.io) to provide you with Quotes, Cat and Dog images. \n \nTo get the messages for :-  \n1.) Quote type in "quote" \n2.) Cat image type in "cat" \n3.) Dog image type in "dog" \n \nTHANK YOU ❤️️ '
        msg.body(text)
        responded = True

    elif 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True

    elif 'cat' in incoming_msg:
          
            msg.media('https://cataas.com/cat')
            responded = True

    elif 'dog' in incoming_msg:
            
            r = requests.get('https://dog.ceo/api/breeds/image/random')
            data = r.json()
            msg.media(data['message'])
            responded = True

    if not responded:
        msg.body('Sorry! This command is not recognised, please type "Hi" to know the options !!!')
    return str(resp)


if __name__ == '__main__':
    app.run()