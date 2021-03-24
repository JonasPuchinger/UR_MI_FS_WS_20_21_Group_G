# Network Analysis

- `multigraph.py`: script to generate a multigraph (multiple types of edges: follower relationships, mentions, replies, quote tweets) based on all tweets and accounts in our dataset.

    Output file: `multi_graph.gexf`

- `multigraph_covid.py`: script to generate a multigraph (multiple types of edges: follower relationships, mentions, replies, quote tweets) based on identified COVID-tweets and all accounts in our dataset.

    Output file: `multi_graph_covid.gexf`

- `multigraph_non_covid.py`: script to generate a multigraph (multiple types of edges: follower relationships, mentions, replies, quote tweets) based on identified non-COVID-tweets and all accounts in our dataset.

    Output file: `multi_graph_non_covid.gexf`

- `multigraph_communities.py`: script to analyse the communities in a given network graph via the Infomap algorithm for community detection. Annotates the respective communities in the output graph. Needs to be run after the scripts mentioned above, because it relies on the output from those scripts.

    Output files: 
    - `communities_multigraph_directed.gexf`
    - `communities_multigraph_covid_directed.gexf`
    - `communities_multigraph_non_covid_directed.gexf`