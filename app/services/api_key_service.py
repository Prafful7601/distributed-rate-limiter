API_KEYS = {
    "free_user": {
        "limit": 10,
        "window": 60
    },
    "pro_user": {
        "limit": 50,
        "window": 60
    },
    "enterprise_user": {
        "limit": 200,
        "window": 60
    }
}


def get_api_key_config(api_key):

    if api_key in API_KEYS:
        return API_KEYS[api_key]

    return {
        "limit": 10,
        "window": 60
    }