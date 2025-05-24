class ApiError(Exception):
    code = 422
    description = "Error"

    def __str__(self):
        return self.description


class Unauthorized(ApiError):
    code = 403
    description = "Token no válido"


class EmailNotFound(ApiError):
    code = 404
    description = "Correo no encontrado"
