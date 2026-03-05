class InvalidUsername(Exception):
    def __init__(self, msg="The username entered does not match your username"):
        self.msg = msg
        super().__init__(self.msg)