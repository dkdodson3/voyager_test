from typing import List, Dict
from unittest.mock import MagicMock

import pytest
from requests import Response, Session

#### Be sure to marek the methods module as sources root ####
from gist_routes import get_gist_data


def get_fake_gist_list(
        *,
        amount: int = 1,
        change_list: List[Dict] = None
):
    """
    Get some gist_items

    I would actually use more pydantic to set up these items but I will assume that not everyone knows that library...
    Pydantic os great for schema builing and valudation
    :param amount: int
    :param change_list: List[Dict]
    :return: List[Dict]
    """
    gist_item = {
        'url': 'https://api.github.com/gists/cdd4017293d51a2c7edcee3509278524',
        'forks_url': 'https://api.github.com/gists/cdd4017293d51a2c7edcee3509278524/forks',
        'commits_url': 'https://api.github.com/gists/cdd4017293d51a2c7edcee3509278524/commits',
        'id': 'cdd4017293d51a2c7edcee3509278524', 'node_id': 'G_kwDOAFXx09oAIGNkZDQwMTcyOTNkNTFhMmM3ZWRjZWUzNTA5Mjc4NTI0',
        'git_pull_url': 'https://gist.github.com/cdd4017293d51a2c7edcee3509278524.git',
        'git_push_url': 'https://gist.github.com/cdd4017293d51a2c7edcee3509278524.git',
        'html_url': 'https://gist.github.com/cdd4017293d51a2c7edcee3509278524',
        'files': {
            'gistfile1.txt': {
                'filename': 'gistfile1.txt',
                'type': 'text/plain',
                'language': 'Text',
                'raw_url': 'https://gist.githubusercontent.com/dkdodson3/cdd4017293d51a2c7edcee3509278524/raw/c3715b404b2b4b281bfdf6f09c01634c8ab0390b/gistfile1.txt',
                'size': 4
            }
        },
        'public': False, 'created_at': '2022-06-01T23:19:20Z',
        'updated_at': '2022-06-01T23:19:20Z', 'description': 'aaa1', 'comments': 0, 'user': None,
        'comments_url': 'https://api.github.com/gists/cdd4017293d51a2c7edcee3509278524/comments',
        'owner': {
            'login': 'dkdodson3',
            'id': 5632467,
            'node_id': 'MDQ6VXNlcjU2MzI0Njc=',
            'avatar_url': 'https://avatars.githubusercontent.com/u/5632467?v=4',
            'gravatar_id': '',
            'url': 'https://api.github.com/users/dkdodson3',
            'html_url': 'https://github.com/dkdodson3',
            'followers_url': 'https://api.github.com/users/dkdodson3/followers',
            'following_url': 'https://api.github.com/users/dkdodson3/following{/other_user}',
            'gists_url': 'https://api.github.com/users/dkdodson3/gists{/gist_id}',
            'starred_url': 'https://api.github.com/users/dkdodson3/starred{/owner}{/repo}',
            'subscriptions_url': 'https://api.github.com/users/dkdodson3/subscriptions',
            'organizations_url': 'https://api.github.com/users/dkdodson3/orgs',
            'repos_url': 'https://api.github.com/users/dkdodson3/repos',
            'events_url': 'https://api.github.com/users/dkdodson3/events{/privacy}',
            'received_events_url': 'https://api.github.com/users/dkdodson3/received_events',
            'type': 'User',
            'site_admin': False
        },
        'truncated': False
    }

    if change_list is not None and len(change_list) != amount:
        raise Exception(f"Invalid items to change. Should be '{amount}' not '{len(change_list)}'")

    ret_val = list()
    if change_list is None:
        for i in range(0, amount):
            gist_item_copy = gist_item.copy()
            gist_item_copy["url"] = f'{gist_item_copy["url"]}{i}'
            ret_val.append(gist_item_copy)
    else:
        changed_dict = gist_item.copy()
        for item in change_list:
            # This will just do a shallow change, and not the nested items
            for key, value in item.values():
                if key in changed_dict:
                    changed_dict[key] = value

        ret_val.append(changed_dict)

    return ret_val


@pytest.mark.asyncio
async def test_gist_valid_urls(token, gist_url, monkeypatch):
    """
    Making sure that no urls coming back from gist are empty
    """

    # Faking out the gist list
    fake_gist_data = get_fake_gist_list(amount=5)
    fake_response = MagicMock(Response)
    fake_response.raise_for_status.return_value = 200
    fake_response.json.return_value = fake_gist_data

    # Faking out the send function with the response I want
    fake_send = MagicMock(Session.send)
    fake_send.return_value = fake_response
    monkeypatch.setattr(Session, "send", fake_send)

    url = f"{gist_url}?per_page=100&page=1"
    params = {
        'per_page': 50,
        'page': 1
    }

    urls = list()
    gist_data = await get_gist_data(url=url, token=token, params=params)
    for gist_value in gist_data:
        if gist_value["url"]:
            val = gist_value["url"]
            urls.append(val)

    # Validate that that no urls for the gists are missing or empty
    assert len(urls) == len(gist_data)