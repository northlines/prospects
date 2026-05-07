from core.logger import get_logger

class AppException(Exception):

    def __init__(self, message: str, code: str, status: int = 400, log:bool = True):
        self.message = message
        self.code = code
        self.status = status

        if log:
            get_logger().error(
                f"[FlixbeeException - {code}] {message}"
            )
            
        super().__init__(message)