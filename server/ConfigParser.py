import json

class ConfigParser():
    def __init__(self, filepath):
        self._filepath = filepath
        
    def load(self):
        infile = open(self._filepath, "r")
        self._config = json.load(infile)
        #handle exceptions here
        #
        #
        infile.close()
        print("!Configuration file loaded")
        return self._config.copy()

    def getConfig(self):
        return self._config.copy()

    def __str__(self):
        return json.dumps(self._config)

