import os
import requests


class TumblrScrape:
    """Class for Tumblr Web Scraper"""

    def __init__(self, api_key=None):
        # API Key is mandatory
        try:
            assert api_key
        except AssertionError:
            raise RuntimeError("API KEY must be supplied")
        self.api_key = api_key

    def getPosts(self, blog, offset=None, before=None):
        """Return dictionary representing posts for specific blog."""
        reqString = f"https://api.tumblr.com/v2/blog/{blog}"
        reqString += f"/posts/text?api_key={self.api_key}&filter=text"

        if offset:
            reqString += f"&offset=${offset}"
        if before:
            reqString += f"&before=${before}"

        r = requests.get(reqString)

        while r.status_code == 429:
            if r.headers['X-Ratelimit-Perday-Remaining'] == 0:
                raise TimeoutError("Reached daily request limit")
            elif r.headers['X-Ratelimit-Perhour-Remaining'] == 0:
                reset = r.headers['X-Ratelimit-Perhour-Reset']
                remaining = r.headers['X-Ratelimit-Perday-Remaining']
                warnString = f"Reached hourly limit, sleeping for {reset}."
                warnString += f"\n{remaining} requests available today."
                raise Warning(warnString)

                os.sleep(reset)
            r = requests.get(reqString)

        if r.status_code == 200:
            return r.json()['response']['posts']

        return None

    def paginate(self, blog, before=None):
        """Paginate all posts up to N."""


def main():
    from dotenv import dotenv_values
    tumblr_config = dotenv_values('.env.tumblr')
    print(tumblr_config)
    tumblr = TumblrScrape(**tumblr_config)

    testPosts = tumblr.getPosts('prokopetz')
    print(testPosts)


if __name__ == "__main__":
    main()
