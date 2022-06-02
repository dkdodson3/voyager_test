import pytest


@pytest.fixture(scope="session", name="gist_url")
def gist_url_fixture() -> str:
    return "https://api.github.com/gists"


@pytest.fixture(scope="module", name="token")
def github_token_fixture() -> str:
    return 'bibbitybobbityboo'