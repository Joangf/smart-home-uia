# Base
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

# 404 
class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class DeviceNotFoundException(NotFoundException):
    def __init__(self, device_id: int):
        super().__init__(f"Device {device_id} not found")

class SensorNotFoundException(NotFoundException):
    def __init__(self, sensor_id: int):
        super().__init__(f"Sensor {sensor_id} not found")

# 400 
class ValidationException(AppException):
    def __init__(self, message: str = "Validation failed", status_code: int = 400):
        super().__init__(message, status_code)

class DuplicateDeviceException(ValidationException):
    def __init__(self, name: str):
        super().__init__(f"Device '{name}' already exists")

class InvalidTokenException(ValidationException):
    def __init__(self):
        super().__init__("Invalid authentication token", status_code=401)

class ExpiredTokenException(ValidationException):
    def __init__(self):
        super().__init__("Token expired", status_code=401)

# 500
class DatabaseException(AppException):
    def __init__(self, message: str = "Database error"):
        super().__init__(message, status_code=500)