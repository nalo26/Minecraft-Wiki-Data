def response(success: bool = True, message: str = "", code: int = 200, **kwargs):
    data = {"success": success}
    if message:
        data["message"] = message
    data.update(kwargs)
    return data, code
