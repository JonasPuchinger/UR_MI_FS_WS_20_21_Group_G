# Assets

- `mdbs_data.json`: list of all members of the German parliament (Bundestag) with a Twitter account. The list includes name, Twitter handle, Twitter ID and politicial party. (may be inaccurate now, because some politicians delete or change their accounts)

- `additional_politicians.json`: list of politicians who are not mebers of the parliament, but we wanted to include nonetheless, because they have popular and/or active Twitter accounts. The list includes name, Twitter handle, Twitter ID and politicial party.

- `all_politicians.json`: combined list of `mdbs_data.json` and `additional_politicians.json`

- `news_portals.json`: list of German news portals for wich we wanted to explore the relationships to the politicians accounts. The list includes name, Twitter handle and politicial party. The list includes name, Twitter handle and Twitter ID.

- `virologists.json`: list of German virologists for wich we wanted to explore the relationships to the politicians accounts. The list includes name, Twitter handle and politicial party. The list includes name, Twitter handle and Twitter ID.

- `wordlist.json`: list of keywords by which we identify COVID-tweets.

- `owid-covid-data-2020.csv`: list of various statistics on COVID-19 case numbers (new cases, deaths, vaccinations, ...). This data is taken from ourworldindata.org (owid). The list is sorted by countries and days. We downloaded all available days for 2020.

- `events.json`: list of important events throughout 2020. Most are related to the pandemic. We identified these events through peaks in COVID-19 case numbers and peaks in the volume of tweets by the politicians. See `/analysis/covid_data_visualized.ipynb` for a visualization of these events.

- `events_covid.json`: subset of `events.json` with only events related to COVID-19. We used this list for figure 5 in our paper.