import requests


def call_external_api(url):
    """

    Args:
        url:

    Returns: API JSON data

    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemError(e)
    return response.json()
