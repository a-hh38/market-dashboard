from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)


def generate_commentary(

    indian_markets,
    global_markets,
    commodities,
    gainers,
    losers

):

    prompt = f"""

You are writing an institutional sell-side market wrap.

Your writing style should resemble:
brokerage research notes,
institutional strategy commentary,
macro desk updates.

Style Guidelines:

- Write in flowing narrative paragraphs
- Mention key global events and market sentiment
- Mention specific index performances
- Mention macro risks
- Mention political commentary if relevant
- Mention commodities and risk appetite
- Mention Indian market context
- Avoid bullet points
- Avoid robotic phrasing
- Avoid generic AI wording
- Sound human and analytical

Example tone:

"Dow Jones fell sharply overnight and recorded its weakest quarterly performance in years while investors continued to assess the economic impact of aggressive monetary tightening. Meanwhile, comments from Federal Reserve officials further dampened sentiment across global equities. Indian indices witnessed a relief rally yesterday, although sustainability remains uncertain amid persistent global macro headwinds."

Now generate today's commentary.

Indian Markets:
{indian_markets}

Global Markets:
{global_markets}

Commodities:
{commodities}

Top Gainers:
{gainers}

Top Losers:
{losers}

Keep commentary:
- concise
- professional
- insightful
- institutional

Maximum:
2 short paragraphs.

"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.9

    )

    return response.choices[0].message.content