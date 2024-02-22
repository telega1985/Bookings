from fastapi import HTTPException, status


class BaseExistsException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseExistsException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class CannotAddDataToDatabase(BaseExistsException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class UserNotFound(BaseExistsException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"


class IncorrectEmailOrPasswordException(BaseExistsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BaseExistsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(BaseExistsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BaseExistsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BaseExistsException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BaseExistsException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class DateFromCannotBeAfterDateTo(BaseExistsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть позже даты выезда"


class CannotBookHotelForLongPeriod(BaseExistsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать отель сроком более месяца"


class CannotProcessCSV(BaseExistsException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"
