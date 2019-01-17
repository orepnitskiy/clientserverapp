import asyncio
def run_server(host:str, port:int):
	"""
	Run server 
	"""
	loop = asyncio.get_event_loop()

	coro = loop.create_server(ClientServerProtocol, host, port)

	server = loop.run_until_complete(coro)

	try:

		loop.run_forever()

	except KeyboardInterrupt:

		pass

	server.close()

	loop.run_until_complete(coro)

	loop.close()
	
	
class ClientServerProtocol(asyncio.Protocol):
	"""
	First two functions get values from
	socket and write data on the socket
	when data is processed
	"""
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data)
        self.transport.write(resp.encode())


def process_data(message):
	""""
	Function that process data, that server
	got from the socket
	"""
	global metrics_list
	message=message.decode()
	if message[0:3]=='put':
		data_prepare=message.split(' ')
		try:
			metrics_list.append([data_prepare[1], data_prepare[2], data_prepare[3]])
		except IndexError:
			return'error\nwrong command\n\n'
		return 'ok\n'
	elif message[0:3]=='get':
		data_output=[]
		data_prepare=message.split(' ')
		try:
			key=data_prepare[1]
		except IndexError:
			return 'error\nwrong command\n\n'
		for i in range(len(metrics_list)):
			for j in range(3):
				if key=='*':				data_output.append(metrics_list[i][j])
				if j==3:
					data_output.append('\n')
				else:
					if key==metrics_list[i][0]:
						data_output.append(metrics_list[i][j])
						if j==3:
							data_output.append('\n')
		return ''.join(data_output)
	else:
		return 'error\nwrong command\n\n'
# run_server('127.0.0.1', 8888)

	
	
	