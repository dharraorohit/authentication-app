from flask import jsonify
from library.main import app

# Custom Exception Classes
class CustomAPIException(Exception):
    def __init__(self, message="An error occurred", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(CustomAPIException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class UnauthorizedError(CustomAPIException):
    def __init__(self, message="Unauthorized access"):
        super().__init__(message, status_code=401)
    
class BadRequest(CustomAPIException):
    def __init__(self, message="Bad request"):
        super().__init__(message=message, status_code=400)

# Error Handlers
@app.errorhandler(CustomAPIException)
def handle_custom_api_exception(error):
    response = {
        "error": error.message,
        "status_code": error.status_code
    }
    return jsonify(response), error.status_code

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    response = {
        "error": "Internal Server Error",
        "status_code": 500
    }
    return jsonify(response), 500

def response_2xx(message="Success", status_code=200, data=None):
    response = {
        "message": message,
        "status_code": status_code,
    }

    if data:
        response["data"] = data

    return jsonify(response), status_code
