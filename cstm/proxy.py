from cstm.input_validator import InputValidator
from cstm.view_interface import ViewInterface

# FIXME: The contents should be updated to something that matches our apps model
INVALID_REQUEST_VALUE = {"session_id": 0}


class Proxy:
    """
    Proxy is meant to be a mediator between the Flask Web Application and the Python backend.
    This class's responsibility is to validate requests before passing them onto component programs.

    Args:
        view_instance: A reference to the application's view
        input_validator: An instance of the view's input validator
    """

    def __init__(self, view_instance: ViewInterface, input_validator: InputValidator):
        self.view_instance = view_instance
        self.input_validator = input_validator

    def create(self, request: dict) -> dict:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        if self.input_validator.validate_create(request):
            return self.view_instance.create(request)
        else:
            return INVALID_REQUEST_VALUE

    def read(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        if self.input_validator.validate_read(request):
            return self.view_instance.read(request)
        else:
            return INVALID_REQUEST_VALUE

    def update(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        if self.input_validator.validate_update(request):
            return self.view_instance.update(request)
        else:
            return INVALID_REQUEST_VALUE

    def delete(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        if self.input_validator.validate_delete(request):
            return self.view_instance.delete(request)
        else:
            return INVALID_REQUEST_VALUE
