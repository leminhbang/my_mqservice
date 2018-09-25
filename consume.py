import time

import pika, os


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # ch.basic_ack(delivery_tag=method.delivery_tag)

url = 'amqp://wjjznskd:VsA6og6dWuLrrlwjcUWZ_ArLyuayquwc@emu.rmq.cloudamqp.com/wjjznskd'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel

# channel.queue_declare(queue='hello')

channel.basic_consume(callback,
                    queue='bang',
                    no_ack=True)

channel.basic_consume(callback, queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()