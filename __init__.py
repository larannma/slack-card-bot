import slack
from flask import Flask, request, jsonify
import random
import threading
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
slack_token = os.getenv("SLACK_TOKEN")

client = slack.WebClient(token=slack_token)

image_urls = [
    'https://ryzhuk.com/wp-content/uploads/2.jpg',
    'https://ryzhuk.com/wp-content/uploads/37.jpg',
    'https://ryzhuk.com/wp-content/uploads/82.jpg',
    'https://ryzhuk.com/wp-content/uploads/78.jpg',
    'https://ryzhuk.com/wp-content/uploads/27-1.jpg',
    'https://ryzhuk.com/wp-content/uploads/31-1.jpg',
    'https://ryzhuk.com/wp-content/uploads/30-1.jpg',
    'https://ryzhuk.com/wp-content/uploads/29-1.jpg',
    'https://ryzhuk.com/wp-content/uploads/h-66.jpg',
    'https://ryzhuk.com/wp-content/uploads/h-68.jpg',
    'https://ryzhuk.com/wp-content/uploads/h-72.jpg',
    'https://ryzhuk.com/wp-content/uploads/h-30.jpg',
    'https://ryzhuk.com/wp-content/uploads/23-2.jpg',
    'https://ryzhuk.com/wp-content/uploads/25-2.jpg',
    'https://ryzhuk.com/wp-content/uploads/47-2.jpg',
]

wishes_and_predictions = [
    "Сегодня благоприятный день для саморазвития и поиска новых знаний. Ваши умственные способности будут на пике, поэтому вам легко усвоить новую информацию и освоить новые навыки. Поэтому не упустите шанс погрузиться в увлекательное чтение или изучение чего-то нового.",
    "Ваше творческое вдохновение сегодня на высоте! Будьте открыты к новым идеям и вдохновению, которое может прийти из неожиданных источников. Это отличное время для творчества, и вы можете создать что-то удивительное, что впечатлит окружающих.",
    "Сегодня отличный день для планирования будущего и постановки целей. Пришло время задуматься о своих желаниях и мечтах, и начать действовать в их направлении. Установите конкретные цели и разработайте план действий для их достижения.",
    "Ваши интуитивные способности сегодня особенно остры. Доверьтесь своей интуиции и внутреннему голосу при принятии решений. Они могут привести вас к правильному выбору и помочь избежать ошибок.",
    "Не бойтесь проявлять инициативу и брать на себя ответственность за свои поступки сегодня. Ваша уверенность и решительность помогут вам достичь успеха в любой сфере жизни.",
    "Сегодняшний день подходит для того, чтобы побаловать себя и позаботиться о своем благополучии. Найдите время для отдыха и расслабления, занимайтесь любимыми хобби и заботьтесь о своем физическом и эмоциональном здоровье.",
    "Ваша способность к адаптации и гибкости будет весьма полезна сегодня. Будьте готовы к неожиданным изменениям и быстро адаптируйтесь к новым обстоятельствам. Это поможет вам преодолеть любые препятствия на пути к успеху.",
    "Сегодняшний день может принести неожиданные возможности для расширения своего круга общения и установления новых контактов. Будьте открыты к новым знакомствам и не стесняйтесь первыми проявлять инициативу в общении.",
    "Вам стоит быть особенно осторожным в финансовых вопросах сегодня. Избегайте рискованных инвестиций и спонтанных расходов. Лучше уделите время анализу своих финансов и разработке более основательного финансового плана.",
    "Сегодняшний день подходит для того, чтобы проявить заботу и внимание к близким людям. Поддержите своих друзей и родных, выслушайте их проблемы и помогите им в решении трудностей.",
    "Ваше чувство ответственности и дисциплины поможет вам достичь целей сегодня. Сосредоточьтесь на своих обязанностях и выполните их качественно и вовремя. Это принесет вам удовлетворение и успех.",
    "Сегодняшний день может быть непредсказуемым, поэтому будьте готовы к любым изменениям в планах и обстоятельствах. Поддерживайте гибкость и адаптируйтесь к новым ситуациям с открытым умом и позитивным настроем.",
    "Ваши коммуникативные навыки сегодня на высоте, и вы сможете успешно договариваться с людьми в любых ситуациях. Воспользуйтесь этим, чтобы добиться желаемого и достигнуть ваших целей.",
    "Сегодняшний день подходит для того, чтобы делать планы на будущее и определять свои приоритеты. Проявите воображение и вообразите свою жизнь через год, пять лет, десять лет. Это поможет вам определиться с целями и планами на будущее.",
    "Ваши творческие способности могут принести вам удивительные результаты сегодня. Разрешите себе мечтать и экспериментировать, и вы откроете для себя новые возможности и перспективы."
]

def send_image_and_button(channel_id, user_id):
    selected_image_url = random.choice(image_urls)
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            # text=f"<@{user_id}> Here's the image:",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user_id}> твоя супер пупер карточка"
                    }
                },
                {
                    "type": "image",
                    "image_url": selected_image_url,
                    "alt_text": "Random Image"
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Разгадка",
                            },
                            "action_id": "show_wish_button",
                            "value": "show_wish_button"
                        }
                    ]
                }
            ]
        )
        print("Image and button sent successfully.")
        return response['ts'], selected_image_url  # Return the timestamp of the message and the URL of the image
    except slack.errors.SlackApiError as e:
        error_message = e.response['error']
        print(f"Error sending image and button to Slack: {error_message}")
        return None, None

def display_wish(channel_id, user_id, message_ts, image_url):
    selected_wish = random.choice(wishes_and_predictions)
    try:
        client.chat_update(
            channel=channel_id,
            ts=message_ts,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user_id}> твоя метафорическая карточка"
                    }
                },
                {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "Random Image"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user_id}> *твое пожелание на сегодня:* {selected_wish}"
                    }
                }
            ]
        )
        print("Wish displayed successfully.")
    except slack.errors.SlackApiError as e:
        error_message = e.response['error']
        print(f"Error updating message in Slack: {error_message}")

@app.route('/new_card', methods=['POST'])
def new_card():
    channel_id = request.form.get('channel_id')
    user_id = request.form.get('user_id')
    threading.Thread(target=send_image_and_button, args=(channel_id, user_id)).start()
    return '', 204

@app.route('/interactive-endpoint', methods=['POST'])
def interactive_endpoint():
    payload = json.loads(request.form['payload'])
    response = payload['actions'][0]
    if response['action_id'] == 'show_wish_button':
        channel_id = payload['channel']['id']
        user_id = payload['user']['id']
        message_ts = payload['message']['ts']
        image_url = payload['message']['blocks'][1]['image_url']  # Extract the image URL from the message
        threading.Thread(target=display_wish, args=(channel_id, user_id, message_ts, image_url)).start()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)