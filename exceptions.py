class DataValidationError(Exception):
    """Raised when input data is invalid or inconsistent."""
    pass


class MappingError(Exception):
    """Raised when test data cannot be mapped to any ideal function."""
    pass
