import requests


def turn_on_plug(config: dict):
    plug_type = config.get('type', 'http')
    if plug_type == 'http':
        url = config.get('url')
        if not url:
            raise RuntimeError('smart plug url missing')
        r = requests.post(url, timeout=10)
        return {'status': 'ok', 'http_status': r.status_code}
    raise RuntimeError(f'Unsupported smart plug type: {plug_type}')
