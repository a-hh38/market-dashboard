def generate_commentary(
    indian_markets,
    global_markets,
    commodities
):

    try:

        nifty = indian_markets[
            indian_markets["market"] == "Nifty"
        ].iloc[0]

        dow = global_markets[
            global_markets["market"] == "Dow Jones"
        ].iloc[0]

        nasdaq = global_markets[
            global_markets["market"] == "Nasdaq"
        ].iloc[0]

        crude = commodities[
            commodities["market"] == "Br. Crude"
        ].iloc[0]

    except Exception:

        return (
            "Global markets traded mixed while investors "
            "continued to assess macroeconomic developments. "
            "Indian equities remained focused on domestic "
            "fundamentals and global risk sentiment."
        )

    commentary_parts = []

    # Global Markets

    if dow["change_1d"] > 1:

        commentary_parts.append(
            "US equities ended higher overnight, supported by positive risk sentiment across major markets."
        )

    elif dow["change_1d"] < -1:

        commentary_parts.append(
            "US equities traded weaker overnight amid cautious investor sentiment and macroeconomic concerns."
        )

    else:

        commentary_parts.append(
            "US markets closed largely mixed as investors evaluated incoming economic data and policy signals."
        )

    # Nasdaq

    if nasdaq["change_1d"] > 1:

        commentary_parts.append(
            "Technology stocks outperformed, with the Nasdaq posting notable gains."
        )

    elif nasdaq["change_1d"] < -1:

        commentary_parts.append(
            "Technology shares remained under pressure, weighing on broader market sentiment."
        )

    # India

    if nifty["change_1d"] > 1:

        commentary_parts.append(
            "Indian equities witnessed broad-based buying interest led by key benchmark constituents."
        )

    elif nifty["change_1d"] < -1:

        commentary_parts.append(
            "Domestic equities faced selling pressure as investors remained cautious."
        )

    else:

        commentary_parts.append(
            "Indian markets traded in a relatively range-bound manner despite mixed global cues."
        )

    # Crude

    if crude["change_1d"] > 2:

        commentary_parts.append(
            "Crude oil prices moved higher and remain an important macro variable for inflation expectations."
        )

    elif crude["change_1d"] < -2:

        commentary_parts.append(
            "Crude oil prices softened, providing some relief to inflation concerns."
        )

    return " ".join(commentary_parts)