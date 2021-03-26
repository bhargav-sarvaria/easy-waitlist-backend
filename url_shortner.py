import requests

api_key = "3a5a2d615b48dce29b1c6398ff6dc8b27ee8d"


def shorten(url):
    try:
        api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
        data = requests.get(api_url).json()["url"]
        if data["status"] == 7:
            shortened_url = data["shortLink"]
            print("Shortened URL:", shortened_url)
            return shortened_url
        else:
            print("[!] Error Shortening URL:", data)
    except Exception as e:
        return 'False'
    return 'False'