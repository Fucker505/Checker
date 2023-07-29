import asyncio
import random
import string
from aiohttp import ClientSession, ClientResponse
from enum import Enum
from re import search
from typing import Callable, List, Union, Optional, Dict, Any


class RequestMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class Checker:
    @staticmethod
    def close_session(session: ClientSession) -> None:
        """Close an aiohttp ClientSession.

        Args:
            session (ClientSession): The aiohttp ClientSession to close.

        Returns:
            None
        """
        if isinstance(session, ClientSession):
            asyncio.create_task(session.close())

    @staticmethod
    async def exec_request(
        url: str,
        method: RequestMethods,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        session: Optional[ClientSession] = None,
        close_session: bool = False,
    ) -> ClientResponse:
        """
        Execute an HTTP request using aiohttp.

        Args:
            url (str): The URL for the request.
            method (RequestMethods): The HTTP method for the request.
            headers (Dict[str, str], optional): Optional headers for the request.
            data (Any, optional): Optional data to send in the request body.
            params (Dict[str, Any], optional): Optional query parameters for the request.
            session (ClientSession, optional): Optional aiohttp ClientSession to reuse the same session.
            close_session (bool, optional): Whether to close the session after the request is done.

        Returns:
            ClientResponse: The aiohttp ClientResponse.
        """
        assert isinstance(
            method, RequestMethods
        ), "You must provide a valid HTTP method!"
        if headers is not None:
            assert isinstance(
                headers, dict
            ), "You must provide a valid dictionary of headers!"
        if params is not None:
            assert isinstance(
                params, dict
            ), "You must provide a valid dictionary of params!"
        if session is None:
            session = ClientSession()
        else:
            assert isinstance(
                session, ClientSession
            ), "You must provide a valid ClientSession!"
        req = await session.request(
            url=url, method=method.value, headers=headers, data=data, params=params
        )
        if close_session:
            asyncio.create_task(session.close())
            session = None
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
        assert isinstance(text, str), "The argument 'text' must be a string."
        assert isinstance(a, str), "The argument 'a' must be a string."
        assert isinstance(b, str), "The argument 'b' must be a string."

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
            *args: Additional arguments to pass to the coroutine function.

        Returns:
            List: A list of results from each coroutine.
        """
        assert isinstance(func, Callable) and isinstance(
            quantity, int
        ), "The 'func' parameter must be a Callable, and 'quantity' must be an integer."
        tasks = [func(*args) for _ in range(quantity)]
        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    async def get_bin(bin_i: str) -> Union[dict, None, bool]:
        """
        Get information about a BIN.

        Args:
            bin_i (str): The BIN.

        Returns:
            Union[dict, None, bool]: A dictionary containing information about the BIN if found,
            None if the request was unsuccessful,
            or False if the BIN number is not valid.
        """
        bin_i = search(r"\b[3-7]\d{5,15}\b", bin_i)
        if not bin_i:
            return False
        bin_i = bin_i.group()
        resp = await Checker.exec_request(
            f"https://bins.antipublic.cc/bins/{bin_i}",
            RequestMethods.GET,
            close_session=True,
        )
        if resp.status == 200:
            return await resp.json()
        else:
            return None
