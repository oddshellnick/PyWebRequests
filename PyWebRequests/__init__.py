import requests
from bs4 import BeautifulSoup
from lxml import etree


def get_file(url: str, headers: dict | None = None, proxies: dict | None = None) -> requests.Response:
    """
    Retrieves content from a given URL.

    Args:
        url (str): The URL to fetch.
        headers (dict, optional): HTTP headers to include in the request. Defaults to None.
        proxies (dict, optional): Proxies to use for the request. Defaults to None.

    Returns:
        requests.Response: The response object from the request.

    :Usage:
        response = get_file("https://www.example.com")
        response = get_file("https://www.example.com", headers={"User-Agent": "MyBot"})
        response = get_file("https://www.example.com", proxies={"http": "http://10.10.1.10:3128"})
    """
    return requests.get(url=url, headers=headers, proxies=proxies)


def get_html(url: str, headers: dict | None = None, proxies: dict | None = None) -> etree._Element:
    """
    Fetches a URL and parses the content into an lxml ElementTree object.

    Args:
        url (str): The URL to fetch.
        headers (dict, optional): HTTP headers to include in the request. Defaults to None.
        proxies (dict, optional): Proxies to use for the request. Defaults to None.

    Returns:
         etree._Element:  An lxml ElementTree object representing the parsed HTML.

    :Usage:
        tree = get_html("https://www.example.com")
    """
    return etree.HTML(
        str(BeautifulSoup(requests.get(url=url, headers=headers, proxies=proxies).content, "html.parser"))
    )


def find_web_elements(etree_: etree._Element, xpath: str) -> list[etree._Element]:
    """
    Finds all web elements matching a given XPath expression.

    Args:
        etree_ (etree._Element): The lxml ElementTree object to search within.
        xpath (str): The XPath expression to use.

    Returns:
        list[etree._Element]: A list of lxml ElementTree objects matching the XPath.

    :Usage:
         elements = find_web_elements(tree, "//a")
    """
    return etree_.xpath(xpath)


def find_web_element(etree_: etree._Element, xpath: str) -> etree._Element | None:
    """
    Finds the first web element matching a given XPath expression.

    Args:
        etree_ (etree._Element): The lxml ElementTree object to search within.
        xpath (str): The XPath expression to use.

    Returns:
        etree._Element | None: The first matching lxml ElementTree object, or None if no match is found.

    :Usage:
        element = find_web_element(tree, "//div[@id='main']")

    """
    try:
        return find_web_elements(etree_, xpath)[0]
    except IndexError:
        return None
