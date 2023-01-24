from http import HTTPStatus

from aiohttp import ClientSession


class BelarusbankAPI(object):

    BASE_URL: str = 'https://belarusbank.by'

    @staticmethod
    def create_client_session(func):
        async def wrapper(*args, **kwargs):
            async with ClientSession(base_url=BelarusbankAPI.BASE_URL) as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @classmethod
    @create_client_session
    async def _get(cls, url: str, session: ClientSession = None, **kwargs) -> dict:
        async with await session.get(
            url=url,
            params=kwargs
        ) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()

    @classmethod
    async def get_exchange(cls, city: str) -> dict:
        return await cls._get(url='/api/kursExchange', city=city)
