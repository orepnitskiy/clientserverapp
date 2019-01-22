import asyncio


def run_server(host:str, port:int):
	""" 
	Function that runs server on 
	host and port that're transfered to
	the function 
	   
    """
	loop = asyncio.get_event_loop()
	coro = loop.create_server(ClientServerProtocol, host, port)
	server = loop.run_until_complete(coro)
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	server.close()
	loop.run_until_complete(server_wait_closed())
	loop.close()
	
	
class ClientServerProtocol(asyncio.Protocol):
	""" Class for processing data that're transferred to the function """
	def __init__(self):
		self.metrics_list = []


	def connection_made(self, transport):
		self.transport = transport
	
			
	def data_received(self, data):
		"""
		Function call the function that processing
		data and writing output from the function on the socket

		"""
		msg=data.decode()
		processed_data=self._process_data(msg)
		self.transport.write(processed_data.encode())
		
		
	def _process_data(self, msg):
		"""
		Finally! Function that process data from decoded message
	 	and returns future response from the server
		"""
		if msg[0:3] == 'put':
			data_prepare = msg.strip("\r\n").split(' ')
			print(data_prepare)
			try:
				self.metrics_list.append([data_prepare[0],data_prepare[1],data_prepare[2]])
			except IndexError:
				return'error\nwrong command\n\n'
			return 'ok\n'
		elif msg[0:3]=='get':
			data_output=["ok\n"]
			data_prepare=msg.strip("\r\n").split(' ')
			try:
				key=data_prepare[1]
			except IndexError:
				return 'error\nwrong command\n\n'
			for i in range(len(self.metrics_list)):
				for j in range(3):
					if key=='*':
						data_output.append(self.metrics_list[i][j])
						if j==3:
							data_output.append('\n')
					else:
						if key==self.metrics_list[i][0]:
							data_output.append(self.metrics_list[i][j])
							if j==3:
								data_output.append('\n')
			data_output.append("\n")
			return ''.join(data_output)
		else:
			return 'error\nwrong command\n\n'
# run_server('127.0.0.1', 8888)
	
