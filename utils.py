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

def degree_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: degree for (node, degree) in G.degree()}

def closeness_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: closeness for (node, closeness) in nx.closeness_centrality(G).items()}

def betweenness_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: betweenness for (node, betweenness) in nx.betweenness_centrality(G).items()}

def pagerank_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: pagerank for (node, pagerank) in nx.pagerank(G).items()}

def G_nodes(G: Type[nx.Graph], criteria: str="none") -> List[Dict[str, float]]:
    assert criteria in ["all", "none", "degree", "closeness", "betweenness", "page_rank"]
    centrality_func = {
        "degree": degree_centrality, "closeness": closeness_centrality,
        "betweenness": betweenness_centrality, "page_rank": pagerank_centrality, 
    }

    if criteria == "all":
        node_centrality = {centrality: func(G) for centrality, func in centrality_func.items()}
    elif criteria == "none":
        node_centrality = {}
    else:
        func = centrality_func[criteria]
        node_centrality = {criteria: func(G)}

    nodes = []
    for n in G.nodes():
        nodes.append({
            **{"id": n}, 
            **{centrality: value[n] for centrality, value in node_centrality.items()}
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