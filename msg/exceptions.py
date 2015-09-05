class ServoConfigException(Exception):
    def __init__(self, message=None, missing=None, host=None):
        super(ServoConfigException, self).__init__(message)
        self.missing = missing
        self.host = host
