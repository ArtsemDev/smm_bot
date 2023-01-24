# https://belapb.by/CashExRatesDaily.php?ondate=01/24/2023
from http import HTTPStatus

from aiohttp import ClientSession, TCPConnector


class BelAgroBankAPI(object):

    BASE_URL: str = 'https://belapb.by'

    @staticmethod
    def create_client_session(func):
        async def wrapper(*args, **kwargs):
            async with ClientSession(
                base_url=BelAgroBankAPI.BASE_URL,
                connector=TCPConnector(verify_ssl=False)
            ) as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @classmethod
    @create_client_session
    async def _get(cls, url: str, session: ClientSession = None, **kwargs) -> str:
        async with await session.get(
            url=url,
            params=kwargs
        ) as response:
            if response.status == HTTPStatus.OK:
                return await response.text()

    @classmethod
    async def get_exchange(cls, ondate: str) -> dict:
        import xmltodict
        response = await cls._get(
            url='/CashExRatesDaily.php',
            ondate=ondate
        )
        return xmltodict.parse(response)
