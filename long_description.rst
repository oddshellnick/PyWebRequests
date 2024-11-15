PyWebRequests: Simplified Web Scraping and Requests
===================================================

PyWebRequests is a lightweight Python library designed to simplify common web scraping and request tasks. It builds upon popular libraries like `requests`, `lxml`, and `BeautifulSoup`, providing a cleaner and more convenient interface for fetching and extracting data from websites.


Key Features:
-------------

* **Easy HTML Parsing:**  Quickly parse HTML content using `get_html`, which returns an `lxml` etree object ready for XPath queries.
* **Simplified Element Finding:** Locate specific web elements using `find_web_element` and `find_web_elements`, abstracting away the complexities of XPath handling.
* **Integrated Proxy Support:**  Seamlessly integrate proxies into your requests using the `proxies` parameter in `get_html` and `get_json`.
* **Dynamic User-Agent Generation:**  Easily obtain random user agents using `get_random_user_agent` to avoid being blocked by websites.
* **Free Proxy List Retrieval:** Fetch a list of free proxies with `get_free_proxies`, filtering by protocol if desired.


Installation:
-------------

.. code-block:: bash

    pip install PyWebRequests


Example Usage:
--------------

.. code-block:: python

    from PyWebRequests.functions import find_web_element, get_html
    from PyWebRequests.getters import get_free_proxies, get_random_user_agent

    # Get a random user agent
    user_agent = get_random_user_agent()
    print(f"Using User-Agent: {user_agent}")

    # Fetch free HTTP proxies
    http_proxies = get_free_proxies("http")
    print(f"Found {len(http_proxies)} HTTP proxies")

    # Fetch HTML content using a random user agent and a proxy
    html = get_html("https://www.example.com", headers={"User-Agent": user_agent}, proxies=http_proxies)

    # Find a specific element
    title_element = find_web_element(html, "//title")
    if title_element is not None:
        print(f"Page Title: {title_element.text}")

    # Fetch JSON data
    json_data = get_file("https://api.example.com/data", headers={"User-Agent": user_agent}).json()
    print(f"JSON Data: {json_data}")


Future Notes
------------

PyWebRequests is continually being developed and improved. Future plans include adding support for more advanced scraping techniques, expanding proxy management features, and incorporating additional utilities for handling various web data formats. Contributions and feature requests are welcome!
