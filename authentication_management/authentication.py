from functools import wraps
from jwt import decode
from django.conf import settings


def token_required(func):
    """
    This decorator checks if the token is valid or not
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")

        if token is None:
            return func(request, *args, **kwargs, auth=False)
        else:
            try:
                token = token.split(" ")[1]
                decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                return func(request, *args, **kwargs, auth=True)
            except Exception as e:
                return func(request, *args, **kwargs, auth=False)

    return wrapper
