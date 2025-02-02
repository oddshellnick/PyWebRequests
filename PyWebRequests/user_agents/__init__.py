import re
import random
import typing
from PyWebRequests.user_agents.data import (
	UserAgentBrowser,
	UserAgentEngine,
	UserAgentOS,
	UserAgentSupportedParts
)
from PyWebRequests.user_agents.data_types import (
	supported_ua_browsers,
	supported_ua_engines,
	supported_ua_platforms
)


def generate_yandex_ua() -> str:
	"""
	Generates a Yandex browser user agent string.

	Returns:
		str: Yandex browser user agent string.
	"""
	return f"YaBrowser/{create_browser_version_from_parts(UserAgentBrowser.yandex_versions)}"


def generate_edge_ua() -> str:
	"""
	Generates an Edge browser user agent string.

	Returns:
		str: Edge browser user agent string.
	"""
	return f"Edg/{create_browser_version_from_parts(UserAgentBrowser.edge_versions)}"


def generate_opera_ua() -> str:
	"""
	Generates an Opera browser user agent string.

	Returns:
		str: Opera browser user agent string.
	"""
	return f"Opera/{create_browser_version_from_parts(UserAgentBrowser.opera_versions)}"


def generate_firefox_ua() -> str:
	"""
	Generates a Firefox browser user agent string.

	Returns:
		str: Firefox browser user agent string.
	"""
	return f"Firefox/{create_browser_version_from_parts(UserAgentBrowser.firefox_versions, True)}"


def add_safari_version(
		current_versions: list[str],
		possible_versions: list[typing.Sequence],
		level: int,
		previous_level_not_changed: bool
) -> list[str]:
	"""
	Recursively adds or modifies Safari version parts.

    This function takes a list of existing Safari version parts, a list of possible version parts at each level,
    a current level, and a boolean indicating whether the previous level was changed.
    It recursively modifies or adds version parts based on the possible versions.

    Args:
        current_versions (list[str]): A list of current version parts.
        possible_versions (list[typing.Sequence]): A list of possible version parts at each level.
        level (int): The current level in the version part hierarchy.
        previous_level_not_changed (bool): True if the previous level was not changed, False otherwise.

    Returns:
        list[str]: Modified list of version parts.
	"""
	if previous_level_not_changed and len(current_versions) > level:
		previous_version = current_versions[level]
	
		current_versions[level] = str(
				int(current_versions[level]) +
				random.randint(0, max(possible_versions[level]) - int(current_versions[level]))
		)
	
		if len(possible_versions) >= level + 1:
			current_versions = add_safari_version(
					current_versions,
					possible_versions,
					level + 1,
					previous_version == current_versions[level]
			)
	else:
		if len(current_versions) < len(possible_versions):
			current_versions.append(str(random.choice(possible_versions[level])))
	
		for i in range(level + 1, len(possible_versions) - 1):
			if random.choice([True, False]):
				current_versions.append(str(random.choice(possible_versions[i])))
			else:
				break
	
	return current_versions


def generate_safari_ua(engine_ua: typing.Optional[str] = None) -> str:
	"""
	Generates a Safari browser user agent string.

    This function generates a Safari user agent string, optionally using an existing AppleWebKit version
    from a given engine user agent string.

    Args:
        engine_ua (typing.Optional[str]): An optional engine user agent string, from which to extract AppleWebKit version.

    Returns:
        str: Safari browser user agent string.
	"""
	if engine_ua is None or re.search(r"AppleWebKit/(\d+(?:\.\d+)*)", engine_ua) is None:
		version_parts = [str(random.choice(UserAgentEngine.apple_webkit_versions[0]))]
	
		if random.choice([True, False]):
			version_parts.append(str(random.choice(UserAgentEngine.apple_webkit_versions[1])))
	
			if random.choice([True, False]):
				version_parts.append(str(random.choice(UserAgentEngine.apple_webkit_versions[2])))
	
		safari_version = ".".join(version_parts)
	else:
		webkit_version: list[str] = re.search(r"AppleWebKit/(\d+(?:\.\d+)*)", engine_ua).group(1).split(".")
		webkit_version = add_safari_version(webkit_version, UserAgentBrowser.safari_versions, 0, True)
	
		safari_version = ".".join(webkit_version)
	
	return f"Safari/{safari_version}"


def generate_chrome_ua() -> str:
	"""
	Generates a Chrome browser user agent string.

	Returns:
		str: Chrome browser user agent string.
	"""
	return f"Chrome/{create_browser_version_from_parts(UserAgentBrowser.chrome_versions)}"


def generate_random_browser_ua(
		browser_to_generate: typing.Optional[supported_ua_browsers] = None,
		engine: typing.Optional[supported_ua_engines] = None,
		engine_ua: typing.Optional[str] = None
) -> tuple[str, str]:
	"""
	Generates a random browser user agent string based on the given browser and engine.

    This function generates a user agent string for a specified browser, or a random browser if none is specified.
    It can also generate a user agent string based on the specified engine.

    Args:
        browser_to_generate (typing.Optional[supported_ua_browsers]): The browser for which to generate the user agent.
        engine (typing.Optional[supported_ua_engines]): The engine on which to base the browser choice.
        engine_ua (typing.Optional[str]): An optional engine user agent string, for Safari version generation.

    Returns:
        tuple[str, str]: A tuple containing the generated user agent string and the browser used.

    Raises:
        ValueError: If the provided engine or browser is not supported.
	"""
	if engine is not None and engine not in UserAgentSupportedParts.engine:
		raise ValueError(f"Unsupported engine ({engine})")
	
	if browser_to_generate is None:
		if engine is None:
			browser_to_generate = random.choice(UserAgentSupportedParts.browser)
		elif engine == "AppleWebKit":
			browser_to_generate = random.choice(UserAgentSupportedParts.apple_webkit_browsers)
		elif engine == "Blink":
			browser_to_generate = random.choice(UserAgentSupportedParts.blink_browsers)
		elif engine == "Gecko":
			browser_to_generate = random.choice(UserAgentSupportedParts.gecko_browsers)
	
	if browser_to_generate == "Chrome":
		chrome_ua = generate_chrome_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return " ".join(list(filter(None, [chrome_ua, safari_ua]))), browser_to_generate
	elif browser_to_generate == "Firefox":
		return generate_firefox_ua(), browser_to_generate
	elif browser_to_generate == "Safari":
		return generate_safari_ua(engine_ua), browser_to_generate
	elif browser_to_generate == "Opera":
		chrome_ua = generate_chrome_ua()
		opera_ua = generate_opera_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return " ".join(list(filter(None, [chrome_ua, opera_ua, safari_ua]))), browser_to_generate
	elif browser_to_generate == "Edge":
		chrome_ua = generate_chrome_ua()
		edge_ua = generate_edge_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return " ".join(list(filter(None, [chrome_ua, edge_ua, safari_ua]))), browser_to_generate
	elif browser_to_generate == "Yandex":
		chrome_ua = generate_chrome_ua()
		yandex_ua = generate_yandex_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return " ".join(list(filter(None, [chrome_ua, yandex_ua, safari_ua]))), browser_to_generate
	else:
		raise ValueError(f"Unsupported browser ({browser_to_generate})")


def generate_random_gecko_ua() -> str:
	"""
	Generates a random Gecko engine user agent string.

	Returns:
		str: Gecko engine user agent string.
	"""
	year = random.choice(UserAgentEngine.gecko_versions[0])
	month = random.choice(UserAgentEngine.gecko_versions[1])
	
	if month in [1, 3, 5, 7, 8, 10, 12]:
		day = random.choice(UserAgentEngine.gecko_versions[2][0])
	elif month in [4, 6, 9, 11]:
		day = random.choice(UserAgentEngine.gecko_versions[2][1])
	elif year % 4 == 0:
		day = random.choice(UserAgentEngine.gecko_versions[2][2])
	else:
		day = random.choice(UserAgentEngine.gecko_versions[2][3])
	
	gecko_version = f"{year}{month:02d}{day:02d}"
	return f"Gecko/{gecko_version}"


def generate_random_apple_webkit_ua() -> str:
	"""
	Generates a random AppleWebKit engine user agent string.

	Returns:
		str: AppleWebKit engine user agent string.
	"""
	version_parts = [str(random.choice(part)) for part in UserAgentEngine.apple_webkit_versions]
	
	return f"AppleWebKit/{'.'.join(version_parts)} (KHTML, like Gecko)"


def generate_random_engine_ua(
		engine_to_generate: typing.Optional[supported_ua_engines] = None,
		platform: typing.Optional[supported_ua_platforms] = None
) -> tuple[str, str]:
	"""
	Generates a random engine user agent string based on the given engine and platform.

    This function generates a user agent string for a specified engine, or a random engine if none is specified.
    It can also generate a user agent string based on the specified platform.

    Args:
        engine_to_generate (typing.Optional[supported_ua_engines]): The engine for which to generate the user agent.
        platform (typing.Optional[supported_ua_platforms]): The platform on which to base the engine choice.

    Returns:
        tuple[str, str]: A tuple containing the generated user agent string and the engine used.

	Raises:
        ValueError: If the provided platform or engine is not supported.
	"""
	if platform is not None and platform not in UserAgentSupportedParts.os:
		raise ValueError(f"Unsupported OS ({platform})")
	
	if engine_to_generate is None:
		engine_to_generate = "AppleWebKit" if platform == "IOS" else random.choice(UserAgentSupportedParts.engine)
	
	if engine_to_generate == "AppleWebKit":
		return generate_random_apple_webkit_ua(), engine_to_generate
	elif engine_to_generate == "Gecko":
		return generate_random_gecko_ua(), engine_to_generate
	elif engine_to_generate == "Blink":
		return generate_random_apple_webkit_ua(), engine_to_generate
	else:
		raise ValueError(f"Unsupported engine ({engine_to_generate})")


def generate_ios_ua() -> str:
	"""
	Generates a random iOS platform user agent string.

	Returns:
		str: iOS platform user agent string.
	"""
	ios_version = random.choice(UserAgentOS.ios_versions)
	device, os_prefix = random.choice(UserAgentOS.ios_devices)
	
	return f"{device}; {os_prefix} {ios_version} like Mac OS X"


def generate_android_ua() -> str:
	"""
	Generates a random Android platform user agent string.

	Returns:
		str: Android platform user agent string.
	"""
	android_type = random.choice(["Linux", "Mobile", None])
	android_version = random.choice(UserAgentOS.android_versions)
	device = random.choice(UserAgentOS.android_devices)
	
	return f"{'Linux; ' if android_type == 'Linux' else ''}Android {android_version}{'; Mobile' if android_type == 'Mobile' else ''}; {device}"


def generate_linux_ua() -> str:
	"""
	Generates a random Linux platform user agent string.

	Returns:
		str: Linux platform user agent string.
	"""
	prefix = random.choice(["X11", None])
	linux_distribution = random.choice(UserAgentOS.linux_distributions)
	linux_architecture = random.choice(UserAgentOS.linux_architectures)
	
	return "; ".join(
			list(filter(None, [prefix, linux_distribution, f"Linux {linux_architecture}"]))
	)


def generate_mac_ua() -> str:
	"""
	Generates a random Macintosh platform user agent string.

	Returns:
		str: Macintosh platform user agent string.
	"""
	cpu = random.choice(["Intel", "Apple Silicon"])
	macos_version = random.choice(
			UserAgentOS.mac_os_intel_versions
			if cpu == "Intel"
			else UserAgentOS.mac_os_apple_silicon_versions
	)
	
	return f"Macintosh; {cpu} Mac OS X {macos_version}"


def generate_windows_ua() -> str:
	"""
	Generates a random Windows platform user agent string.

	Returns:
		str: Windows platform user agent string.
	"""
	windows_version = random.choice(UserAgentOS.windows_versions)
	windows_architecture = random.choice(UserAgentOS.windows_architectures)
	
	return f"Windows {windows_version}; {windows_architecture}"


def generate_random_os_ua(os_to_generate: typing.Optional[supported_ua_platforms] = None) -> tuple[str, str]:
	"""
	Generates a random OS user agent string based on the given OS.

	This function generates a user agent string for a specified OS, or a random OS if none is specified.

    Args:
        os_to_generate (typing.Optional[supported_ua_platforms]): The OS for which to generate the user agent.

    Returns:
        tuple[str, str]: A tuple containing the generated user agent string and the OS used.

    Raises:
        ValueError: If the provided OS is not supported.
	"""
	if os_to_generate is None:
		os_to_generate = random.choice(UserAgentSupportedParts.os)
	
	if os_to_generate == "Windows":
		return generate_windows_ua(), os_to_generate
	elif os_to_generate == "Macintosh":
		return generate_mac_ua(), os_to_generate
	elif os_to_generate == "Linux":
		return generate_linux_ua(), os_to_generate
	elif os_to_generate == "Android":
		return generate_android_ua(), os_to_generate
	elif os_to_generate == "IOS":
		return generate_ios_ua(), os_to_generate
	else:
		raise ValueError(f"Unsupported OS ({os_to_generate})")


def generate_random_mozilla_ua() -> str:
	"""
	Generates a basic Mozilla user agent string.

	Returns:
		str: Basic Mozilla user agent string.
	"""
	return "Mozilla/5.0"


def generate_random_user_agent() -> str:
	"""
	Generates a complete random user agent string.

	This function combines the Mozilla, OS, Engine, and Browser user agent parts
	to generate a complete user agent string.

    Returns:
        str: Complete user agent string.
	"""
	mozilla_ua = generate_random_mozilla_ua()
	os_ua, used_os = generate_random_os_ua()
	engine_ua, used_engine = generate_random_engine_ua(platform=used_os)
	browser_ua, used_browser = generate_random_browser_ua(engine=used_engine, engine_ua=engine_ua)
	
	return f"{mozilla_ua} ({os_ua}) {engine_ua} {browser_ua}"


def create_browser_version_from_parts(parts: list[typing.Union[int, range]], drop_last_zero: bool = False) -> str:
	browser_version = [
		str(part)
		if isinstance(part, int)
		else str(random.choice(part))
		for part in parts
	]
	
	if drop_last_zero and browser_version[-1] == 0 and random.choice([True, False]):
		browser_version.pop(-1)
	
	return '.'.join(browser_version)
