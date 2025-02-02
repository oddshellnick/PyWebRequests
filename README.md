# PyWebRequests: Simplified Web Scraping and Requests

PyWebRequests is a lightweight Python library designed to simplify common web scraping and request tasks. It builds upon popular libraries like `requests`, `lxml`, and `BeautifulSoup`, providing a cleaner and more convenient interface for fetching and extracting data from websites.

## Key Features:

* **Easy HTML Parsing:** Quickly parse HTML content using `get_html`, which returns an `lxml` etree object ready for XPath queries.
* **Simplified Element Finding:** Locate specific web elements using `find_web_element` and `find_web_elements`, abstracting away the complexities of XPath handling.
* **Integrated Proxy Support:** Seamlessly integrate proxies into your requests using the `proxies` parameter in `get_html` and `get_json`.
* **Dynamic User-Agent Generation:** Easily obtain random user agents using `get_random_user_agent` to avoid being blocked by websites. This function generates `~5 * 10^777` unique user-agents.
* **Free Proxy List Retrieval:** Fetch a list of free proxies with `get_free_proxies`, filtering by protocol if desired.

## Installation:

* **With pip:**
    ```bash
    pip install PyWebRequests
    ```

* **With git:**
    ```bash
    pip install git+https://github.com/oddshellnick/PyWebRequests.git
    ```

## Example Usage:

```python
from PyWebRequests import find_web_element, get_req, get_html
from PyWebRequests.user_agents import generate_random_user_agent
from PyWebRequests.proxies import get_free_proxies

user_agent = generate_random_user_agent()
print(f"Using User-Agent: {user_agent}")

http_proxies = get_free_proxies("http")
print(f"Found {len(http_proxies)} HTTP proxies")

html = get_html("https://www.example.com", headers={"User-Agent": user_agent}, proxies=http_proxies)

title_element = find_web_element(html, "//title")
if title_element is not None:
    print(f"Page Title: {title_element.text}")

json_data = get_req("https://api.example.com/data", headers={"User-Agent": user_agent}).json()
print(f"JSON Data: {json_data}")
```

## Future Notes

PyWebRequests is continually being developed and improved. Future plans include adding support for more advanced scraping techniques, expanding proxy management features, and incorporating additional utilities for handling various web data formats. Contributions and feature requests are welcome!