import requests
import tempfile


def image_load(url):
    request = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    lf = tempfile.NamedTemporaryFile()
    for block in request.iter_content(1024 * 8):
        if not block:
            break
        lf.write(block)
    return {
        'name': file_name,
        'file': lf
    }