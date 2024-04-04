from typing import Type, List, Dict
import networkx as nx
from pathlib import Path
import json, os, sys
from io import BytesIO
import numpy as np
sys.path.append(os.path.dirname(__file__) + os.sep + './')
from FINDER import FINDER
dqn = FINDER()

def get_network_config(code: str=None) -> Dict:
    code = str(code)
    with open('data/empirical/network_config.json', "r") as json_file:
        network_config = json.load(json_file)
    mapping_dct = {val["code"]: key for key, val in network_config.items()}
    # print(code, mapping_dct.keys())
    if code is None or code not in mapping_dct.keys():
        return network_config
    else:
        network_name = mapping_dct[code]
        return { **network_config[network_name], **{'name': network_name} }

def get_tool_config(chosen_tool_id: str=None) -> Dict:
    with open('_static/tool_config.json', "r") as json_file:
        tool_config = json.load(json_file)
    
    mapping_dct = {val["code"]: key for key, val in tool_config.items()}
    
    if chosen_tool_id is None or chosen_tool_id not in mapping_dct.keys():
        return tool_config
    else:
        tool_name = mapping_dct[chosen_tool_id]
        return { **tool_config[tool_name], **{'name': tool_name} }

def read_sample(path: Path):
    G = nx.read_gml(path)
    relabel_map = {node: str(idx) for idx, node in enumerate(G.nodes())}
    return nx.relabel_nodes(G, relabel_map, copy=True)

def parse_network(network_detail: Dict[str, list]) -> Type[nx.Graph]:
    assert "nodes" in network_detail.keys() and "links" in network_detail.keys()
    # Create an empty graph
    G = nx.Graph()

    # Add nodes to the graph
    for node in network_detail['nodes']:
        G.add_node(node['id'])

    # Add edges to the graph
    for link in network_detail['links']:
        if type(link["source"]) == dict:
            link["source"] = link["source"]["id"]
        if type(link["target"]) == dict:
            link["target"] = link["target"]["id"]
        G.add_edge(link['source'], link['target'])
    return G

def remove_node(G: Type[nx.Graph], node: str) -> Type[nx.Graph]:
    if node in G.nodes():
        G.remove_node(node)
        return G
    else:
        raise ValueError(f"Node {node} is not in the graph")

def degree_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: degree for (node, degree) in G.degree()}

def closeness_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: closeness for (node, closeness) in nx.closeness_centrality(G).items()}

def betweenness_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: betweenness for (node, betweenness) in nx.betweenness_centrality(G).items()}

def pagerank_centrality(G: Type[nx.Graph]) -> Dict[str, float]:
    return {node: pagerank for (node, pagerank) in nx.pagerank(G).items()}

def GCC_size(G: Type[nx.Graph]) -> int:
    if len(list(nx.connected_components(G))) != 0:
        return len(max(nx.connected_components(G), key=len))
    return 1

def G_nodes(G: Type[nx.Graph], criteria: str="NO_HELP") -> List[Dict[str, float]]:
    assert criteria in ["ALL", "NO_HELP", "HDA", "HCA", "HBA", "HPRA"]
    centrality_func = {
        "HDA": degree_centrality, "HCA": closeness_centrality,
        "HBA": betweenness_centrality, "HPRA": pagerank_centrality, 
    }

    if criteria == "ALL":
        node_centrality = {centrality: func(G) for centrality, func in centrality_func.items()}
    elif criteria == "NO_HELP":
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

def hxa_ranking(G: Type[nx.Graph], criteria: str) -> Dict[str, int]:
    assert criteria in ["HDA", "HCA", "HBA", "HPRA"]

    # create a dict to store the ranking
    ranking = {}

    # sort node by the node centrality
    node_lst = sorted(
        G_nodes(G, criteria), 
        key=lambda x: x[criteria], 
        reverse=True
    )

    # assign the ranking
    rank, current_val = 0, None
    for node in node_lst:
        if node[criteria] != current_val:
            rank += 1
            current_val = node[criteria]
        ranking[node["id"]] = rank
    return ranking

def gml_format(G: nx.Graph) -> str:
    gData = {"nodes": G_nodes(G), "links": G_links(G)}
    G = parse_network(gData)
    gml_generator = nx.generate_gml(G) 
    return "\n".join([gml for gml in gml_generator])

def getRobustness(gData: Dict, graph: str, sol: str) -> float:
    path = Path(f"data/empirical/{graph}.gml")
    
    # compute robustness
    full_G = read_sample(path)
    fullGCCsize = GCC_size(full_G)
    G = parse_network(gData)
    G = remove_node(G, node=sol)
    remainGCCsize = GCC_size(G)

    return 1 - remainGCCsize/fullGCCsize

def gameEnd(gData: Dict, sol: str) -> bool:
    G = parse_network(gData)
    G = remove_node(G, sol)
    
    if len(G.edges()) == 0:
        return True
    return False

def finder_ranking(G: Type[nx.Graph], graph: str) -> Dict:
    sols = finder_sol(G, graph)
    ranking = {}
    for i, node in enumerate(sols):
        ranking[str(node)] = i+1
    for node in G.nodes():
        if node not in ranking.keys():
            ranking[str(node)] = len(sols)+1

    return ranking

def finder_sol(G: Type[nx.Graph], graph: str):
    mapping = {node: str(idx) for idx, node in enumerate(G.nodes())}
    reversed_mapping = {str(idx): node for idx, node in enumerate(G.nodes())}
    reorder_G = nx.relabel_nodes(G, mapping, copy=False)

    G_content = BytesIO(gml_format(reorder_G).encode('utf-8'))
    model_file = f'./models/Model_EMPIRICAL/{graph}.ckpt'

    _, sols = dqn.Evaluate(G_content, model_file)
    for idx, sol in enumerate(sols):
        sols[idx] = reversed_mapping[str(sol)]
    return sols

def finderRobustness(gData: Dict, graph: str) -> List[float]:
    G = parse_network(gData) # TODO : payoff 的顯示問題
    sols = finder_sol(G, graph)
    payoff = []
    for sol in sols:
        payoff.append(getRobustness(gData, graph, sol))
    return np.cumsum(payoff).tolist()