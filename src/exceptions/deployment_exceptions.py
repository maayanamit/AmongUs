from fastapi import HTTPException


class InvalidUsername(HTTPException):
    def __init__(self, msg="The username entered does not match your username"):
        self.msg = msg
        super().__init__(status_code=400, detail=self.msg)


class DatabaseExists(HTTPException):
    def __init__(self, msg="There is already a database with that name"):
        self.msg = msg
        super().__init__(status_code=400, detail=self.msg)


class NotFound(HTTPException):
    def __init__(self, msg="There is no a database with that ID"):
        self.msg = msg
        super().__init__(status_code=404, detail=self.msg)