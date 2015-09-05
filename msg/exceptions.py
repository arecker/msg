class ServoConfigException(Exception):
    def __init__(self, message=None, missing=None):
        super(ServoConfigException, self).__init__(message)
        self.missing = missing
