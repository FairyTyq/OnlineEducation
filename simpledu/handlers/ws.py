# coding:utf-8

import redis
import gevent

from flask import Blueprint


ws = Blueprint('ws',__name__,url_prefix='/ws')

# create redis connection
redis = redis.from_url('redis://127.0.0.1:6379')

class Chatroom(object):
	def __init__(self):
		self.clients = []
		# init pubsub system
		self.pubsub = redis.pubsub()
		# subscribe to chat channel
		self.pubsub.subscribe('chat')

	def register(self,client):
		self.clients.append(client)

	def send(self,client,data):
		# send data to every client
		try:
			client.send(data.decode('utf-8'))
		except:
			# error,remove client
			self.clients.remove(client)

	def run(self):
		# send the received message to all clients in turn
		for message in self.pubsub.listen():
			if message['type'] == 'message':
				data = message.get('data')
				for client in self.clients:
					# send message asynchronously with gevent
					gevent.spawn(self.send,client,data)

	def start(self):
		# Execute the run function asynchronously
		gevent.spawn(self.run) 

# init the Chatroom
chat = Chatroom()
# start chat room asynchronously
chat.start()


@ws.route('/send')
def inbox(ws):
	while not ws.closed:
		message = ws.receive()

		if message:
			# send message to chat channnel
			redis.publish('chat',message)


@ws.route('/recv')
def outbox(ws):
	# this function used to register client connection ,
	# also send message which received from Chatroom to these clients
	chat.register(ws)
	while not ws.closed:
		gevent.sleep(0.1)



