from unittest import result

import pika, os, sys


url = 'amqp://wjjznskd:VsA6og6dWuLrrlwjcUWZ_ArLyuayquwc@emu.rmq.cloudamqp.com/wjjznskd'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a ch8annel

message = ' '.join(sys.argv[1:]) or "Hello bang le, !!!"
message_2 = ' '.join(sys.argv[1:]) or "Hello bang, !!!"

exchange = 'my exchange_%s'% 4

# exchange_type = 'direct'
exchange_type = 'topic'
# exchange_type = 'headers'
# exchange_type = 'fanout'

channel.exchange_declare(exchange=exchange,
                         exchange_type=exchange_type)

channel.queue_declare(queue='bang')
channel.queue_bind(exchange=exchange,
                   queue='bang', routing_key='ban*')

channel.queue_declare(queue='hello')
channel.queue_bind(exchange=exchange,
                   queue='hello', routing_key='ban#')

channel.basic_publish(exchange=exchange,
                        routing_key='hello',
                         body=message_2)

def callback_queue():
    print('callback queue')

channel.basic_publish(exchange=exchange,
                        routing_key='bang',
                         body=message,
                      # properties=pika.BasicProperties(
                      #     reply_to=callback_queue,
                      # )
                      )


print(" [x] Sent to queue hello %r" % message_2)
print('sent to queue bang %r' % message)
connection.close()

# fibonacci_rpc = FibonacciRpcClient()
# result = fibonacci_rpc.call(4)
# print("fib(4) is %r" % result)