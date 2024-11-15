import PyWebRequests as request_functions


def get_random_user_agent() -> str | None:
    """
    Retrieves a random user agent string from user-agents.net.

    Returns:
        str | None: A random user agent string.

    :Usage:
        user_agent = get_random_user_agent()
        print(user_agent)
    """
    random_user_agent = request_functions.find_web_element(
        request_functions.get_html("https://useragents.io/random", headers={"User-Agent": "Mozilla/5.0"}),
        '//div[@class="table-responsive"]/table[@class="table table-striped"]/tbody/tr/td/a',
    )

    if random_user_agent is not None:
        return random_user_agent.text
    else:
        return None


def get_free_proxies(protocol: str | list[str] | None = None) -> dict[str, str]:
    """
    Retrieves a list of free proxies from proxifly/free-proxy-list.

    Args:
        protocol (str | list[str] | None): The desired proxy protocol(s).
            If None, returns proxies of all protocols.
            Can be a single protocol string (e.g., "http") or a list of strings (e.g., ["http", "socks4"]).
            Defaults to None.

    Returns:
        dict[str, str]: A dictionary where keys are protocols and values are proxy strings.

    :Usage:
        all_proxies = get_free_proxies()
        http_proxies = get_free_proxies("http")
        http_and_socks_proxies = get_free_proxies(["http", "socks4"])

        print(all_proxies)
        print(http_proxies)
        print(http_and_socks_proxies)
    """
    proxies = request_functions.get_file(
        url="https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.json",
        headers={"User-Agent": get_random_user_agent()},
    ).json()

    if protocol is None:
        return {proxy["protocol"]: proxy["proxy"] for proxy in proxies}
    elif isinstance(protocol, list):
        return {
            proxy["protocol"]: proxy["proxy"] for proxy in filter(lambda proxy: proxy["protocol"] in protocol, proxies)
        }
    else:
        return {
            proxy["protocol"]: proxy["proxy"] for proxy in filter(lambda proxy: proxy["protocol"] == protocol, proxies)
        }
