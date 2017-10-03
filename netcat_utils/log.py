import logging
import os
class Logger():
    def __init__(self, name, level, log_file, format=None):
        self.name = name
        self.level = level
        self.log_file = log_file
        if format is None:
            self.format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        else: self.format = format

    def boostrap(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path_file = dir_path +"/%s" % self.log_file

        if  not os.path.exists(path_file):
            open(path_file,'a').close()

        # create logger
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        # create a file handler
        handler = logging.FileHandler(self.log_file)
        handler.setLevel(self.level)

        # create a logging format
        formatter = logging.Formatter(self.format)
        handler.setFormatter(formatter)

        # add the hanlders to the logger
        logger.addHandler(handler)

        return logger