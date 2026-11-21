from __future__ import print_function

import json
import sys

try:
    import urllib.request as urllib_request
    _default_urlopen = urllib_request.urlopen
except (ImportError, AttributeError):
    import urllib
    _default_urlopen = getattr(urllib, "urlopen", None)

accessToken = "TOKENVALUE"  # YOUR ACCESS TOKEN GETS INSERTED HERE
limit = 100


def get_likes_on_FB(userId, accessToken="TOKENVALUE", limit=100, opener=None):
    """Fetch and print likes and shares for a Facebook user's posts.

    Preconditions and Contracts (by source line):
        - Line 8: userId (str) identifies the Facebook user account.
        - Line 7: accessToken (str) authenticates the Graph API request.
        - Line 9: limit (int) sets the maximum number of posts requested.
        - Lines 11-18: Constructs Graph API endpoint URL.
        - Line 19: opener retrieves JSON payload; defaults to urllib.request.urlopen.
        - Line 20: Counter id starts at 0.
        - Line 22: Prints initial '0'.
        - Line 24: data['data'] contains list of post objects.
        - Lines 25-27: 'created_time' string sliced into time, date, and year.
        - Lines 29-32: 'shares' count extracted if present, else 0.
        - Lines 33-36: 'likes' count extracted if present, else 0.
        - Line 37: id incremented per post.
        - Lines 38-48: Tab-separated post metrics printed to stdout.

    Args:
        userId (str): The Facebook user ID.
        accessToken (str, optional): Facebook Graph API access token. Defaults to "TOKENVALUE".
        limit (int, optional): Post query limit. Defaults to 100.
        opener (callable, optional): Dependency injection seam for HTTP requests.
            Defaults to None (falls back to urllib.request.urlopen).

    Returns:
        list[dict]: Parsed post records containing id, time, date, year, shares, likes, and formatted.
    """
    if opener is None:
        opener = _default_urlopen

    url = (
        "https://graph.facebook.com/"
        + str(userId)
        + "/posts?access_token="
        + str(accessToken)
        + "&limit="
        + str(limit)
    )

    response = opener(url)
    if hasattr(response, "read"):
        raw_data = response.read()
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode("utf-8")
        data = json.loads(raw_data)
    elif isinstance(response, str):
        data = json.loads(response)
    elif isinstance(response, dict):
        data = response
    else:
        data = json.load(response)

    id = 0
    print(str(id))

    records = []
    items = data.get("data", [])
    for item in items:
        created_time = item.get("created_time", "")
        time = created_time[11:19]
        date = created_time[5:10]
        year = created_time[0:4]

        if "shares" in item:
            num_share = item["shares"]["count"]
        else:
            num_share = 0

        if "likes" in item:
            num_like = item["likes"]["count"]
        else:
            num_like = 0

        id += 1

        time_str = time if isinstance(time, str) else time.decode("utf-8")
        date_str = date if isinstance(date, str) else date.decode("utf-8")
        year_str = year if isinstance(year, str) else year.decode("utf-8")

        formatted_line = (
            str(id)
            + "\t"
            + time_str
            + "\t"
            + date_str
            + "\t"
            + year_str
            + "\t"
            + str(num_share)
            + "\t"
            + str(num_like)
        )
        print(formatted_line)
        records.append({
            "id": id,
            "time": time_str,
            "date": date_str,
            "year": year_str,
            "shares": num_share,
            "likes": num_like,
            "formatted": formatted_line,
        })

    return records


if __name__ == "__main__":
    if len(sys.argv) > 1:
        userId = sys.argv[1]
    else:
        userId = ""
    get_likes_on_FB(userId)
