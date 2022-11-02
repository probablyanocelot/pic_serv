import pika
import base64
from dotenv import load_dotenv
import os
import json
import encoding

from config import cloudAMQP
from main import Image, db


params = pika.URLParameters(
    f'{ cloudAMQP }?heartbeat=1')

# params = pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, credentials=pika.credentials.PlainCredentials(
#     MQ_USER, MQ_PASSWD), heartbeat_interval=0)
# conn = pika.BlockingConnection(parameters=params)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='pic-serv')


def callback(ch, method, properties, body):
    print('Received in pic_serv')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'image/jpeg':
        image_title = data['title']
        image_string = data['image']
        image_path = './img/'

        # Encode image_string to bytes
        encoding.string_to_bytes(image_string, image_path + image_title)

        # Fill in model
        picture = Image(
            title=image_title, image='path placeholder')

        # Add to db
        db.session.add(picture)
        db.session.commit()
        print('Image Created')

    elif properties.content_type == 'picture_updated':
        picture = Image.query.get(data['id'])
        picture.title = data['title']
        picture.image = data['image']
        db.session.commit()
        print('Image Updated')

    elif properties.content_type == 'picture_deleted':
        picture = Image.query.get(data)
        db.session.delete(picture)
        db.session.commit()
        print('Image Deleted')


channel.basic_consume(queue='pic-serv',
                      on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
