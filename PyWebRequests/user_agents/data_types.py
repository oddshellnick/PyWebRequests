import typing


supported_ua_platforms = typing.Union[typing.Literal["Windows", "Macintosh", "Linux", "Android", "IOS"], str]
supported_ua_engines = typing.Union[typing.Literal["AppleWebKit", "Gecko", "Blink"], str]
supported_ua_browsers = typing.Union[
	typing.Literal["Chrome", "Firefox", "Safari", "Opera", "Edge", "YandexBrowser"],
	str
]
