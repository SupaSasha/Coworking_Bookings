from datetime import datetime

from fastapi import HTTPException


class BookingException(Exception):
    detail = "Unexpected mistake"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingException):
    detail = "Object not found"


class WorkplaceNotFoundException(BookingException):
    detail = "Workplace not found"


class CoworkingNotFoundException(BookingException):
    detail = "Coworking not found"


class ObjectAlreadyExistsException(BookingException):
    detail = "A similar object already exists"


class AllWorkplacesAreBookedException(BookingException):
    detail = "There are no workplaces left available"


class IncorrectTokenException(BookingException):
    detail = "Incorrect Token"


class EmailNotRegisteredException(BookingException):
    detail = "The user with this email is not registered."


class IncorrectPasswordException(BookingException):
    detail = "IncorrectPassword"


class UserAlreadyExistsException(BookingException):
    detail = "User Already Exists"


def check_date_to_after_date_from(datetime_from: datetime, datetime_to: datetime) -> None:
    if datetime_to <= datetime_from:
        raise HTTPException(status_code=422, detail="The time interval is set incorrectly")


class BookinglHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CoworkingNotFoundHTTPException(BookinglHTTPException):
    status_code = 404
    detail = "Coworking not found"


class WorkplaceNotFoundHTTPException(BookinglHTTPException):
    status_code = 404
    detail = "Workspace not found"


class AllWorkplacesAreBookedHTTPException(BookinglHTTPException):
    status_code = 409
    detail = "There are no workplaces left available"


class IncorrectTokenHTTPException(BookinglHTTPException):
    detail = "IncorrectToken"


class EmailNotRegisteredHTTPException(BookinglHTTPException):  # noqa: F821
    status_code = 401
    detail = "The user with this email is not registered"


class UserEmailAlreadyExistsHTTPException(BookinglHTTPException):
    status_code = 409
    detail = "The user with this email already exists"


class IncorrectPasswordHTTPException(BookinglHTTPException):
    status_code = 401
    detail = "Incorrect Password"


class NoAccessTokenHTTPException(BookinglHTTPException):
    status_code = 401
    detail = "You have not provided an access token"
