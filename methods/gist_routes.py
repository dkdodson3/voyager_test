from typing import Union, List, Dict

import requests
from requests import Response
from typeguard import typechecked


@typechecked
async def get_gist_data(url: str, token: str, params: dict = None, headers: dict = None) -> Union[List, Dict]:
    """
    Getting the data for a specific url
    :param url: str
    :param token: str
    :param params: dict
    :param headers: dict
    :return: Union[List, Dict]
    """
    # Unfortunately requests does not have as good of support for async, so I would use httpx. But we will pretend...
    if not isinstance(headers, dict):
        headers = dict()

    headers['Authorization'] = f'token {token}'

    if not isinstance(params, dict):
        params = dict()

    if 'per_page' not in params.keys():
        params['per_page'] = 100

    response: Response = requests.request("GET", url, headers=headers, params=params)
    response.raise_for_status()
    ret_data = response.json()

    return ret_data