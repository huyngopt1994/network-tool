import os
import logging

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer

from threading import Thread

log = logging.getLogger(__name__)

class CustomFtpServer(Thread):
    def __init__(self, user,
                 passwd, home_dir=None,
                 address=None, port=None):
        Thread.__init__(self)
        self.daemon =True

        self.user = user
        self.passwd = passwd
        self.home_dir = home_dir if home_dir else '/tmp'
        self.address = address if address else '0.0.0.0'
        self.port = port if port else 9100
        check_dir(self.home_dir)

        authorizer = DummyAuthorizer()
        authorizer.add_user(self.user, self.passwd, self.home_dir, perm='elradfmw')

        handler = FTPHandler
        handler.authorizer = authorizer
        self.server = FTPServer((self.address,self.port), handler)

    def run(self):
        Thread.run(self)
        self.server.serve_forever()

def check_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e :
            log.error("Can't create this directory: ", e)
            exit(1)



