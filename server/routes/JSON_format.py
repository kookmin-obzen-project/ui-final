from fastapi.responses import JSONResponse
def JSON_format(message: str, data = {}):
    response = {
        "message": message,
        "data": data
    }
    return response