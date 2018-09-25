#
# import pika
# import sys
#
# # connection = pika.BlockingConnection(pika.ConnectionParameters(host='emu-01.rmq.cloudamqp.com'))
#
# url = 'amqp://wjjznskd:VsA6og6dWuLrrlwjcUWZ_ArLyuayquwc@emu.rmq.cloudamqp.com/wjjznskd'
# params = pika.URLParameters(url)
# connection = pika.BlockingConnection(params)
#
# channel = connection.channel()
#
# channel.queue_declare(queue='bang', durable=True)
#
# message = ' '.join(sys.argv[1:]) or "Hello bang!"
# channel.basic_publish(exchange='amq.direct',
#                       routing_key='hello',
#                       body=message,
#                       properties=pika.BasicProperties(
#                          delivery_mode=2,
#                       ))
# print(" [x] Sent %r" % message)
# connection.close()


import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        url = 'amqp://wjjznskd:VsA6og6dWuLrrlwjcUWZ_ArLyuayquwc@emu.rmq.cloudamqp.com/wjjznskd'
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.exchange = 'my exchange_%s' % 4

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange,
                                 exchange_type='topic')
        result = self.channel.queue_declare('bang')
        self.channel.queue_bind(exchange=self.exchange,
                           queue='bang', routing_key='ban*')
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key='bang',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib ")
response = fibonacci_rpc.call(10)
print(" [.] Got %r" % response)