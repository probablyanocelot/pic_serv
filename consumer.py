import pika
from dotenv import load_dotenv
import os
import json

from config import cloudAMQP
from main import Picture, db


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

    if properties.content_type == 'picture_created':
        picture = Picture(
            id=data['id'], title=data['title'], image=data['image'])
        db.session.add(picture)
        db.session.commit()
        print('Picture Created')

    elif properties.content_type == 'picture_updated':
        picture = Picture.query.get(data['id'])
        picture.title = data['title']
        picture.image = data['image']
        db.session.commit()
        print('Picture Updated')

    elif properties.content_type == 'picture_deleted':
        picture = Picture.query.get(data)
        db.session.delete(picture)
        db.session.commit()
        print('Picture Deleted')


channel.basic_consume(queue='pic-serv',
                      on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
