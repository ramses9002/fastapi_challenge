def response_success(data=None, message=None):
    return {
        "status": True,
        "data": data,
        "message": message
    }


def response_error( data=None, message=None):
    return {
        "status": False,
        "data": data,
        "message": message or "Ocurrió un error inesperado"
    }