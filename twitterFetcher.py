#import tweepy

## Replace with your Bearer Token
#bearer_token = "AAAAAAAAAAAAAAAAAAAAAISa4wEAAAAAq67lggW3H1v0FcIMTL%2F7WPrgrp8%3DsUAzk90wvERoR84RL2o4vQ7sDd4TgUTmCjkOtsrSYWL4nqCZmq"

#client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAISa4wEAAAAAq67lggW3H1v0FcIMTL%2F7WPrgrp8%3DsUAzk90wvERoR84RL2o4vQ7sDd4TgUTmCjkOtsrSYWL4nqCZmq")

## Example: Fetch tweet by ID
#tweet_id = "1979466306580607447"  # extract from URL
#tweet = client.get_tweet(tweet_id, expansions=["attachments.media_keys"], media_fields=["url", "type"])

#print(tweet.data)  # Text content
#if "media" in tweet.includes:
    #for media in tweet.includes["media"]:
        #print(media.type, media.url)









#import snscrape.modules.twitter as sntwitter
#print("snscrape works!")

#tweet_id = "1979466306580607447"
#for tweet in sntwitter.TwitterTweetScraper(tweet_id).get_items():
    #print(tweet.content)
    #if tweet.media:
        #for m in tweet.media:
            #print(m)






# Requires: pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, Tuple, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_tweet_text_and_media(url: str, nitter_mirrors=None, timeout=10) -> Tuple[Optional[str], Dict]:
    """
    Attempts to fetch tweet text and media URLs from a public X (twitter) status URL.
    Tries, in order:
      1) Twitter oEmbed
      2) Nitter mirrors (if provided / defaults)
      3) Direct page meta tags and common HTML selectors

    Returns (text_or_None, {"source": "...", "media": [list of media URLs]})
    """
    if nitter_mirrors is None:
        # A small selection of known nitter mirrors; availability changes.
        nitter_mirrors = [
            "https://nitter.net",
            "https://nitter.snopyta.org",
            "https://nitter.1d4.us",
            "https://nitter.eu"
        ]

    result_meta = {"source": None, "media": []}

    # 1) Try Twitter oEmbed
    try:
        oembed_url = "https://publish.twitter.com/oembed"
        r = requests.get(oembed_url, params={"url": url, "omit_script": "true"}, headers=HEADERS, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            html = data.get("html", "")
            # html contains quoted text/html snippet — extract visible text
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            if text:
                result_meta["source"] = "oembed"
                return text, result_meta
    except Exception:
        pass  # fallthrough to next approach

    # 2) Try Nitter mirrors
    # convert https://x.com/user/status/id or https://twitter.com/... to nitter path
    try:
        # Extract path after domain
        m = re.search(r"https?://(?:www\.)?[^/]+/(.+)$", url)
        if m:
            path = m.group(1)
            # remove any leading query params
            path = path.split("?")[0]
            for mirror in nitter_mirrors:
                try:
                    nitter_url = mirror.rstrip("/") + "/" + path
                    r = requests.get(nitter_url, headers=HEADERS, timeout=timeout)
                    if r.status_code != 200:
                        continue
                    soup = BeautifulSoup(r.text, "html.parser")
                    # On Nitter, tweet text usually appears in <div class="tweet-content"> or <div class="tweet-content media-body">
                    content = soup.find("div", class_=re.compile(r"tweet-content|tweet-text|content"))
                    if content:
                        text = content.get_text(" ", strip=True)
                        # find images
                        media = []
                        for img in content.find_all("img"):
                            src = img.get("src")
                            if src:
                                # make absolute
                                if src.startswith("//"):
                                    src = "https:" + src
                                elif src.startswith("/"):
                                    src = mirror.rstrip("/") + src
                                media.append(src)
                        result_meta["source"] = f"nitter:{mirror}"
                        result_meta["media"] = media
                        if text:
                            return text, result_meta
                except Exception:
                    continue
    except Exception:
        pass

    # 3) Last fallback: direct page scraping (og:description / twitter:description / meta tags)
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            # First try meta tags
            meta = None
            for prop in ("og:description", "twitter:description", "description"):
                tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
                if tag and tag.get("content"):
                    meta = tag["content"]
                    break
            if meta:
                # meta may contain "Tweet by @user: TEXT"
                # strip common prefixes like "“" or '“' or '...' and the username
                cleaned = re.sub(r"^\"?Tweet by @[^:]+:?\s*", "", meta).strip()
                result_meta["source"] = "meta"
                return cleaned, result_meta

            # If not in meta, try common HTML selectors (this may break often)
            # X uses heavy JS; sometimes tweet text appears inside <div data-testid="tweetText">
            tweet_text_divs = soup.find_all("div", attrs={"data-testid": "tweetText"})
            if tweet_text_divs:
                text = " ".join(div.get_text(" ", strip=True) for div in tweet_text_divs)
                result_meta["source"] = "page:data-testid"
                return text, result_meta

            # As a last attempt, search for <meta property="og:title"> or <meta name="title">
            title_tag = soup.find("meta", attrs={"property": "og:title"}) or soup.find("title")
            if title_tag:
                title_text = title_tag.get("content") if title_tag.get("content") else title_tag.get_text()
                if title_text:
                    cleaned = re.sub(r"^Twitter / X:\s*", "", title_text).strip()
                    result_meta["source"] = "title"
                    return cleaned, result_meta

        else:
            raise Exception(f"Failed to fetch page: {r.status_code}")
    except Exception as exc:
        # final fallback: show error
        return None, {"source": "error", "error": str(exc)}

    return None, {"source": "unknown"}

def tweetFetcher(test_url):
    #test_url = "https://x.com/GrahamSmith_/status/1979466306580607447"
    print("test url:", test_url)
    text, meta = get_tweet_text_and_media(test_url)
    print("source:", meta.get("source"))
    if text:
        print("tweet text:", text)
        #print(text)
        return text
    else:
        print("Could not extract tweet text. meta:", meta)
        return meta


# Example usage:
#testUrl = "https://x.com/GrahamSmith_/status/1979466306580607447"

#tweetFetcher(testUrl)