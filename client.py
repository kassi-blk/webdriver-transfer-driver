from selenium import webdriver
from time import sleep
import socket
from selenium.webdriver.remote.errorhandler import ErrorHandler

class RemoteExisting (webdriver.remote.webdriver.WebDriver):
    def __init__(
        self,
        session_id,
        command_executor="http://127.0.0.1:4444",
        desired_capabilities=None,
        browser_profile=None,
        proxy=None,
        keep_alive=True,
        file_detector=None,
    ):
        capabilities = {}
        _ignore_local_proxy = False
        self.command_executor = command_executor
        if isinstance(self.command_executor, (str, bytes)):
            self.command_executor = \
                webdriver.remote.webdriver.get_remote_connection(
                    capabilities,
                    command_executor=command_executor,
                    keep_alive=keep_alive,
                    ignore_local_proxy=_ignore_local_proxy,
                )
        self.session_id = session_id
        self.error_handler = ErrorHandler()
        pass

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        print('Trying to connect to the data server...')
        conn.connect(('localhost', 25255))
    except ConnectionRefusedError:
        print('No connection to the server. A request will be repeated after 5 seconds')
        sleep(5)
    else:
        print('Connected successfully')
        break
try:
    print('Waiting for a data...');
    data = conn.recv(1024)
except:
    exit(-1)
else:
    conn.close()
url = data.split()[0].decode('utf-8')
sid = data.split()[1].decode('utf-8')
print('The data has been received')
print('Executor\'s URL: ' + str(url) + '.')
print('Session ID: ' + str(sid) + '.')
print('Connecting to the existing WebDriver...')
d = RemoteExisting(sid, command_executor=url)
# Just let's say
print('Done')

sleep(5)

d.get('https://www.gnu.org')

sleep(5)

d.close()
