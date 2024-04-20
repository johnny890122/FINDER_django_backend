from typing import Type, List, Dict
import networkx as nx
from pathlib import Path
import json, os, sys
from io import BytesIO
import numpy as np
from scipy.integrate import simpson as simpson

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

def network_detail(network_id: str) -> Dict[str, list]:
    network_name = get_network_config(network_id)["name"]
    G =read_sample(f"data/empirical/{network_name}.gml")
    network_detail = {
        "nodes": G_nodes(G), "links": G_links(G), "name": network_name, 
    }
    return network_detail

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

    return nodes

def G_links(G: Type[nx.Graph]) -> List[Dict[str, int]]:
    links = []
    for (i, j) in G.edges():
        links.append({"source": i, "target": j})
    
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

def getRobustness(G: nx.Graph, graph: str) -> float:
    full_G = read_sample(f"data/empirical/{graph}.gml")
    fullGCCsize = GCC_size(full_G)
    remainGCCsize = GCC_size(G)

    return 1 - remainGCCsize/fullGCCsize

def getHumanPayoff(graph_name: str, all_chosen_node: List[str]) -> float:
    all_robustness = [0]

    G = read_sample(Path(f"data/empirical/{graph_name}.gml"))
    for chosen_node in all_chosen_node:
        G = remove_node(G, chosen_node)
        all_robustness.append(getRobustness(G, graph_name))

    return simpson(all_robustness) / len(all_robustness)

def getInstantFinderPayoff(graph_name: str, all_chosen_node: List[str]) -> List[float]:
    payoff_lst, all_robustness = [], [0]
    
    G = read_sample(Path(f"data/empirical/{graph_name}.gml"))
    for chosen_node in all_chosen_node:
        G = remove_node(G, str(chosen_node))
        all_robustness.append(getRobustness(G, graph_name))
        payoff = simpson(all_robustness) / len(all_robustness)
        payoff_lst.append(payoff)
    
    sols = finder_sol(G.copy(), graph_name)
    for sol in sols:
        G = remove_node(G, str(sol))
        all_robustness.append(getRobustness(G, graph_name))
        payoff = simpson(all_robustness) / len(all_robustness)
        payoff_lst.append(payoff)
    
    return payoff_lst

def gameEnd(graph_name: str, all_chosen_node: List[str]) -> bool:
    G = read_sample(f"data/empirical/{graph_name}.gml")
    for node in all_chosen_node:
        G = remove_node(G, str(node))
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

def getFinderPayoff(graph_name: str) -> List[float]:
    payoff_lst, all_robustness = [], [0]
    
    G = read_sample(Path(f"data/empirical/{graph_name}.gml"))
    sols = finder_sol(G, graph_name)
    for sol in sols:
        G = remove_node(G, str(sol))
        all_robustness.append(getRobustness(G, graph_name))
        payoff = simpson(all_robustness) / len(all_robustness)
        payoff_lst.append(payoff)

    return payoff_lst