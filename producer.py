import pika
import json
import ssl


from config import cloudAMQP
# from config import cloudAMQP_host, cloudAMQP_v_host, cloudAMQP_user, cloudAMQP_pass


params = pika.URLParameters(cloudAMQP)

connection = pika.BlockingConnection(params)


# Create the channel and the queue
channel = connection.channel()
channel.queue_declare(queue='pic-serv')

# # publish the message
# channel.basic_publish(exchange='',
#                       routing_key='pic-serv',
#                       body='Hello World!')

# print(" [x] Sent 'Hello World!'")
# connection.close()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='pic-serv', body=json.dumps(body), properties=properties)
    # print(" [x] Sent %r" % body)


# import ssl

# credentials = pika.credentials.PlainCredentials(
#     username=cloudAMQP_user, password=cloudAMQP_pass)

# params = pika.ConnectionParameters(
#     host=f'{cloudAMQP_host}.rmq.cloudamqp.com',
#     port=5671,
#     virtual_host=cloudAMQP_v_host,
#     credentials=credentials,
#     # ssl=True
# )


# connection = pika.BlockingConnection(parameters)

# # Create the channel and the queue
# channel = connection.channel()
# channel.queue_declare(queue='hello', durable=True)

# # publish the message
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')

# print(" [x] Sent 'Hello World!'")
# connection.close()
