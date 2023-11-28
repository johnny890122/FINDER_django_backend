from typing import Type, List, Dict
import networkx as nx
from pathlib import Path
import json

def get_network_config():
    with open('network_data/empirical/network_config.json', "r") as json_file:
        network_config = json.load(json_file)
    return network_config

def read_sample(path: Path):
    G = nx.read_gml(path)
    relabel_map = {node: int(idx) for idx, node in enumerate(G.nodes())}
    return nx.relabel_nodes(G, relabel_map, copy=True)

def G_nodes(G: Type[nx.Graph]) -> List[Dict[str, int]]:
    degree = {node: degree for (node, degree) in G.degree()}
    closeness = {node: closeness for (node, closeness) in nx.closeness_centrality(G).items()}
    betweenness = {node: betweenness for (node, betweenness) in nx.betweenness_centrality(G).items()}
    pagerank = {node: pagerank for (node, pagerank) in nx.pagerank(G).items()}

    nodes = []
    for n, _ in list(G.nodes(data=True)):
        nodes.append({
            "id": n, "degree": degree[n], "closeness": closeness[n], 
            "betweenness": betweenness[n], "page_rank": pagerank[n]
        })

    # # add a pesudo node as center node
    # if len(list(nx.connected_components(G))) > 1:
    #     nodes.append({
    #         "id": "source", "degree": -1, "closeness": -1, "betweenness": -1, "page_rank": -1, "display": "False"
    #     })

    return nodes

def G_links(G: Type[nx.Graph]) -> List[Dict[str, int]]:
    links = []
    for (i, j) in G.edges():
        links.append({"source": i, "target": j})
    
    # if len(list(nx.connected_components(G))) > 1:
    #     for CC in nx.connected_components(G):
    #         subgraph = G.copy().subgraph(CC)
    #         # find highest degree node 
    #         keys = list(nx.degree_centrality(subgraph).keys())
    #         values = list(nx.degree_centrality(subgraph).values())
    #         node = keys[ np.argmax(values)]
    #         links.append({"source": "source", "target": node, 'dashed': "False", "display": "False"})
    return links