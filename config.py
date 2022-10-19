from os import getenv
from dotenv import load_dotenv

load_dotenv()

cloudAMQP = getenv('RABBITMQ_URI')

cloudAMQP_host = getenv('CLOUD_AMQP_HOST')
cloudAMQP_v_host = getenv('CLOUD_AMQP_V_HOST')
cloudAMQP_user = getenv('CLOUD_AMQP_USER')
cloudAMQP_pass = getenv('CLOUD_AMQP_PASS')

postgres_uri = getenv('POSTGRES')
