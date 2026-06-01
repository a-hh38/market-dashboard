def generate_economic_snippets(released_events):

    snippets = []

    for _, row in released_events.iterrows():

        country = str(row.get("country", "")).strip()
        event = str(row.get("title", "")).strip()

        actual = str(row.get("actual", "")).strip()
        forecast = str(row.get("forecast", "")).strip()

        if actual == "":
            continue

        try:

            actual_num = float(actual)
            forecast_num = float(forecast)

            if actual_num > forecast_num:

                snippet = (
                    f"{country} {event} came in above "
                    f"consensus expectations "
                    f"({actual} vs {forecast})."
                )

            elif actual_num < forecast_num:

                snippet = (
                    f"{country} {event} came in below "
                    f"consensus expectations "
                    f"({actual} vs {forecast})."
                )

            else:

                snippet = (
                    f"{country} {event} was broadly "
                    f"in line with expectations."
                )

        except:

            snippet = (
                f"{country} {event} reported "
                f"an actual reading of {actual}."
            )

        snippets.append(snippet)

    return snippets[:8]