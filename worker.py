import pika
import time
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='task_queue', durable=True)
# print(' [*] Waiting for messages. To exit press CTRL+C')
#
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     time.sleep(body.count(b'.'))
#     print(" [x] Done")
#     ch.basic_ack(delivery_tag = method.delivery_tag)
#
# channel.basic_qos(prefetch_count=1)
# channel.basic_consume(callback,
#                       queue='bang')
#
# channel.start_consuming()

import pika


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)
    exchange = 'my exchange_%s' % 4
    ch.basic_publish(exchange=exchange,
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id
                     ),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


url = 'amqp://wjjznskd:VsA6og6dWuLrrlwjcUWZ_ArLyuayquwc@emu.rmq.cloudamqp.com/wjjznskd'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a ch8annel

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='bang')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
