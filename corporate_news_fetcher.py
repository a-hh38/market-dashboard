import feedparser

EXCLUDE_KEYWORDS = [

    "share price",
    "live updates",
    "stocks to watch",
    "bullish",
    "bearish",
    "rsi",
    "target",
    "buy ",
    "sell ",
    "technical",
    "outlook",
    "trading idea",
    "top picks"
]


RSS_FEEDS = [

    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",

    "https://www.moneycontrol.com/rss/business.xml"
]


def is_relevant(headline):

    text = headline.lower()

    return not any(
        keyword in text
        for keyword in EXCLUDE_KEYWORDS
    )


def remove_duplicates(news):

    seen = set()

    unique = []

    for item in news:

        key = item["headline"].lower()

        if key not in seen:

            seen.add(key)

            unique.append(item)

    return unique


def fetch_corporate_news():

    news = []

    for url in RSS_FEEDS:

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:30]:

                news.append({

                    "headline": entry.title,

                    "link": entry.link,

                    "published":
                        getattr(
                            entry,
                            "published",
                            ""
                        )
                })

        except Exception as e:

            print(f"RSS Error: {e}")

    news = [
        item
        for item in news
        if is_relevant(item["headline"])
    ]

    news = remove_duplicates(news)

    return news[:12]


if __name__ == "__main__":

    news = fetch_corporate_news()

    print(
        f"Fetched {len(news)} stories\n"
    )

    for item in news:

        print(item["headline"])