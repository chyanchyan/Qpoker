import configparser


class Config:
    def __init__(self, filepath):
        self.filepath = filepath
        self.config = configparser.ConfigParser.read(filenames=filepath)


