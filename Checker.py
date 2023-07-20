import asyncio
import random
import string
from aiohttp import ClientSession, ClientResponse
from enum import Enum
from typing import List, Callable

class RequestMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class Checker:
    def __init__(self, cc: str, mes: str, ano: str, cvv: str) -> None:
        """
        Initialize the Checker object with credit card information.

        Args:
            cc (str): Credit card number as a string.
            mes (str): Expiry month as a string.
            ano (str): Expiry year as a string.
            cvv (str): CVV as a string.

        Raises:
            TypeError: If any of the arguments is not a string.
        """
        if not all(isinstance(x, str) for x in [cc, mes, ano, cvv]):
            raise TypeError("Invalid type data!")
        self.cc = cc
        self.mes = mes
        self.ano = ano
        self.cvv = cvv
        self.email = self._get_random_email()
        self.session = None

    def close_connection(self) -> None:
        """
        Close the HTTP session if it's open.
        """
        if self.session:
            asyncio.create_task(self.session.close())
            self.session = None

    @staticmethod
    async def exec_request(
        url: str, method: RequestMethods, headers: dict = None, data=None, session=None
    ) -> ClientResponse:
        """
        Execute an HTTP request using aiohttp.

        Args:
            url (str): The URL for the request.
            method (RequestMethods): The HTTP method for the request.
            headers (dict, optional): Optional headers for the request.
            data (any, optional): Optional data to send in the request body.
            session (ClientSession, optional): Optional aiohttp ClientSession to reuse the same session.

        Returns:
            ClientResponse: The aiohttp ClientResponse.
        """
        assert isinstance(method, RequestMethods), "You must provide a valid HTTP method!"
        if headers is not None:
            assert isinstance(
                headers, dict
            ), "You must provide a valid dictionary of headers!"
        if session is None:
            session = ClientSession()
        else:
            assert isinstance(
                session, ClientSession
            ), "You must provide a valid ClientSession!"
        req = await session.request(url=url, method=method.value, headers=headers, data=data)
        return req

    @staticmethod
    def get_str(text: str, a: str, b: str) -> str:
        """
        Get the substring between two strings a and b from text.

        Args:
            text (str): The input text to extract the substring from.
            a (str): The start string of the substring.
            b (str): The end string of the substring.

        Returns:
            str: The extracted substring.
        """
        return text.split(a)[1].split(b)[0]

    @staticmethod
    def get_random_email() -> str:
        """
        Generate a random email address.

        Returns:
            str: A random email address.
        """
        return (
            "".join(random.choice(string.ascii_letters) for _ in range(15))
            + "@gmail.com"
        )

    @staticmethod
    def create_headers_easy(headers_to_create: str) -> dict:
        """
        Create a dictionary of headers from a formatted string.

        Args:
            headers_to_create (str): The formatted string containing headers.

        Returns:
            dict: The dictionary of headers.
        """
        assert isinstance(
            headers_to_create, str
        ), "You must provide a valid string of headers!"
        headers_created = {}
        lines = headers_to_create.strip().split("\n")
        for line in lines:
            i = line.find(":")
            headers_created[line[:i].strip()] = line[i + 1 :].strip()
        return headers_created
    
    @staticmethod
    async def massRequests(func: Callable, quantity: int = 10, *args) -> List:
        """
        Perform multiple asynchronous requests.

        Args:
            func (Callable): The coroutine function to execute in each request.
            quantity (int, optional): The number of requests to perform. Default is 10.

        Returns:
            List: A list of results from each coroutine.
        """
        assert isinstance(func, Callable) and isinstance(quantity, int), "The 'func' parameter must be a Callable, and 'quantity' must be an integer."
        tasks = [func(args) for _ in range(quantity)]
        results = await asyncio.gather(*tasks)
        return results
    
