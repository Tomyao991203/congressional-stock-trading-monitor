class InputValidator:
    """ InputValidator is an abstract base class meant to define the interface for validating input in the Congressional
    Stock Trading Monitor.
    """

    def validate_create(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: True if the input correctly matches the implementation's input specs for read operations,
                 False otherwise.
        """
        raise NotImplementedError

    def validate_read(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: True if the input correctly matches the implementation's input specs for read operations,
                 False otherwise.
        """
        raise NotImplementedError

    def validate_update(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: True if the input correctly matches the implementation's input specs for read operations,
                 False otherwise.
        """
        raise NotImplementedError

    def validate_delete(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: True if the input correctly matches the implementation's input specs for read operations,
                 False otherwise.
        """
        raise NotImplementedError
