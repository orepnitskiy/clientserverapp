import time
import socket
class ClientError(Exception):
	pass
class Client:
	def __init__(self, ip, port, timeout=None):
		self.ip=ip
		self.port=int(port)
		self.timeout=int(timeout)
	def send(self, cmd):
		with socket.create_connection((self.ip, self.port), self.timeout) as sock:
			sock.sendall(cmd.encode('utf8'))
			confirmation_from_serv=sock.recv(1024)
		return confirmation_from_serv.decode("utf8")
	def put(self, name, number, timestamp=str(int(time.time()))):
		response=self.send(f"put {name} {number} {timestamp}\n")
		if response[0:3]!="ok\n":
			raise ClientError(response)
	def get(self, key):
		metrics_dict=dict()
		response=self.send(f'get {key}\n')
		if response[0:3]!="ok\n":
			raise ClientError(response)
		metrics=response.split('\n')
		for line in metrics[1:-2]:
			metric=line.split(' ')
			server_key=metric[0]
			server_value=float(metric[1])
			server_timestamp=int(metric[2])
			if not server_key in metrics_dict:
				metrics_dict[server_key]=[]
			metrics_dict[server_key].append((server_timestamp, server_value))
		return metrics_dict
				
		