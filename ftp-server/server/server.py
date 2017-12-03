import argparse
import logging
import sys
from serverlib import  CustomFtpServer

log = logging.getLogger('ftp-server')

class VastParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--address",
                        help="adress for ftp server, default: 0.0.0.0:9100")
    parser.add_argument("-u","--user", required=True,
                        help="user for ftp server")
    parser.add_argument("-p","--pasword",required=True,
                        help="password for ftp server")
    parser.add_argument("-d","--directory",
                        help="home directory for ftp server,default: /tmp/")

    options = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)

    host, port = (options.address.split(":",2)
                  if options.address else None,None)

    if port:
        try :
            port = int(port)
        except Exception:
            parser.error('port is invalid not interger')

    ftpserver = CustomFtpServer(options.user,
                                options.password,
                                options.directory,
                                host, port)
    log.info('ftp server was created')

    try:
        ftpserver.run()
    except (KeyboardInterrupt,SystemExit):
        log.info("Shutting down")
        sys.exit(0)

if __name__ == '__main__':
    main()