import re


CORPORATE_RULES = {

    "acquisition": [
        "acquire",
        "acquired",
        "acquires",
        "buy stake",
        "purchase stake"
    ],

    "partnership": [
        "partnership",
        "collaboration",
        "alliance",
        "joint venture"
    ],

    "order_win": [
        "wins order",
        "order worth",
        "contract",
        "award"
    ],

    "fund_raise": [
        "qip",
        "rights issue",
        "fund raise",
        "preferential issue"
    ],

    "dividend": [
        "dividend"
    ],

    "board_meeting": [
        "board meeting"
    ],

    "product_launch": [
        "launches",
        "introduced",
        "new product"
    ]
}


def classify_corporate(headline):

    text = headline.lower()

    for category, keywords in CORPORATE_RULES.items():

        for keyword in keywords:

            if keyword in text:
                return category

    return "general"


def classify_economic(actual, forecast):

    if forecast is None:
        return "neutral"

    if actual > forecast:
        return "positive_surprise"

    elif actual < forecast:
        return "negative_surprise"

    return "inline"