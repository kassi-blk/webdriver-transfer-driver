from selenium import webdriver
import socketserver

class ThreadedTCPRequestHandler (socketserver.BaseRequestHandler):
    def handle (self):
        print('A new connection has been handled')
        d = self.server.mycustomdata
        data = '%s %s' %(d.command_executor._url, d.session_id)
        print('Sending a data to client...')
        self.request.sendall(bytes(data, 'utf-8'))
        input('Press ENTER to shutdown the server and end WebDriver session')
        self.server.shutdown()

class ThreadedTCPServer (socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass;

d = webdriver.Chrome('./chromedriver')
d.get('https://www.python.org')

server = ThreadedTCPServer(('localhost', 25255), ThreadedTCPRequestHandler)
server.mycustomdata = d
print('Waiting for a connection...')
server.serve_forever()
