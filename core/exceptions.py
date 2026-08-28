from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        request = context.get("request")
        if request is not None and request.method == "DELETE":
            exc = PermissionDenied("; ".join(exc.messages))
        else:
            detail = getattr(exc, "message_dict", None) or exc.messages
            exc = DRFValidationError(detail)
    return drf_exception_handler(exc, context)
