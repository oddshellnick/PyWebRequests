import PyWebRequests as request_functions
from PyWebRequests.user_agents import generate_random_user_agent


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
	proxies = request_functions.get_req(
			url="https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.json",
			headers={"User-Agent": generate_random_user_agent()},
	).json()
	
	if protocol is None:
		return {proxy["protocol"]: proxy["proxy"] for proxy in proxies}
	elif isinstance(protocol, list):
		return {
			proxy["protocol"]: proxy["proxy"]
			for proxy in filter(lambda proxy: proxy["protocol"] in protocol, proxies)
		}
	else:
		return {
			proxy["protocol"]: proxy["proxy"]
			for proxy in filter(lambda proxy: proxy["protocol"] == protocol, proxies)
		}
