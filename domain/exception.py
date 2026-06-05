class DomainError(Exception):
    pass


class UserNotFoundError(DomainError):
    pass


class WrongPasswordError(DomainError):
    pass


class UserAlreadyExistsError(DomainError):
    pass


class ProfileNotFoundError(DomainError):
    pass


class SanatoriumNotFoundError(DomainError):
    pass


class InvalidRequestError(DomainError):
    pass
