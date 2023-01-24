# ?lat=<value>&lon=<value>&<params>
from http import HTTPStatus

from aiohttp import ClientSession


class NominatimAPI(object):

    BASE_URL: str = 'https://nominatim.openstreetmap.org'

    @staticmethod
    def create_client_session(func):
        async def wrapper(*args, **kwargs):
            async with ClientSession(
                base_url=NominatimAPI.BASE_URL,
                headers={'Accept-Language': 'ru'}
            ) as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @classmethod
    @create_client_session
    async def _get(cls, url: str, session: ClientSession = None, **kwargs) -> dict | list:
        async with await session.get(
            url=url,
            params=kwargs
        ) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()

    @classmethod
    async def get_reverse(
            cls,
            lat: float,
            lon: float,
            format_: str = 'json'
    ) -> dict:
        return await cls._get(url='/reverse', **{'lat': lat, "lon": lon, 'format': format_})

    @classmethod
    async def get_search(
            cls,
            city: str,
            format_: str = 'json'
    ) -> list:
        return await cls._get(url='/search', **{'city': city, 'format': format_})

