import time

from twisted.internet import reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory


class Client(protocol.Protocol):
	"""Once connected, send a message, then print the result."""

	def __init__(self, master_sender=False):
		self.master_sender = master_sender

	def connectionMade(self):
		pass
		# string = f"hello from {self.transport.getPeer().port} - {self.master_sender}"
		# self.transport.write(string.encode('ascii'))

	def dataReceived(self, data):
		"""As soon as any data is received, write it back."""
		print("Server said:", data)

	def connectionLost(self, reason):
		print("connection lost")


class Factory(ReconnectingClientFactory):
	master_sender = None

	def __init__(self, master_sender=False):
		self.master_sender = master_sender

	def buildProtocol(self, addr):
		self.resetDelay()
		return Client(self.master_sender)

	def clientConnectionLost(self, connector, reason):
		print('Lost connection.  Reason:', reason)
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		print('Connection failed. Reason:', reason)
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


if __name__ == '__main__':

	def initFunction():
		while True:
			print('yo')
			time.sleep(1)

	f = Factory()
	for x in range(1, 26):
		reactor.connectTCP("localhost", 3000 + x, f)
	reactor.connectTCP("localhost", 4000, f)

	# reactor.callWhenRunning(initFunction)
	reactor.run()
