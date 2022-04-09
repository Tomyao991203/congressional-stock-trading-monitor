class ViewInterface:
    """ ViewInterface is an abstract base class meant to define the interface for the main application views.
    These views could include: Viewing all transactions, viewing all traded companies/tickers, 
    and viewing all representatives.
    """

    def create(self, request: dict) -> dict:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        raise NotImplementedError

    def read(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        raise NotImplementedError

    def update(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        raise NotImplementedError

    def delete(self, request: dict) -> bool:
        """
        :param request: dictionary containing implementation specific request information.
        :return: dictionary containing the implementation specific request response.
        """
        raise NotImplementedError
