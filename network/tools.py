
# -*- coding: utf-8 -*-
# @Time    : 2022/1/19 21:30
# @Author  : pcy
# @Site    : 
# @File    : tools.py
# @Software: PyCharm 
# @Comment : 

import networkx
import network.dao as network_dao
import pandas as pd
import matplotlib.pyplot as plt

from network.models import NetworkEdge, NetworkNode

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, EdgesAndLinkedNodes, NodesAndLinkedEdges
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from bokeh.embed import components
from networkx.algorithms import community
from bokeh.models import EdgesAndLinkedNodes, NodesAndLinkedEdges



def convert_to_G(edge_info):
    df = pd.DataFrame(edge_info.values())
    G = networkx.from_pandas_edgelist(df, 'source', 'target')
    return G


def draw_the_network(G):
    # 计算度
    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)

    # 调整
    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, degree + number_to_adjust_by) for node, degree in networkx.degree(G)])
    networkx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    # 计算community
    communities = community.greedy_modularity_communities(G)

    # 给节点添加颜色等属性
    # Create empty dictionaries
    modularity_class = {}
    modularity_color = {}
    # Loop through each community in the network
    for community_number, a_community in enumerate(communities):
        # For each member of the community, add their community number and a distinct color
        for name in a_community:
            modularity_class[name] = community_number
            modularity_color[name] = Spectral8[community_number]

    # Add modularity class and color as attributes from the network above
    networkx.set_node_attributes(G, modularity_class, 'modularity_class')
    networkx.set_node_attributes(G, modularity_color, 'modularity_color')


    # Choose colors for node and edge highlighting
    node_highlight_color = 'white'
    edge_highlight_color = 'black'

    # Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'modularity_color'

    # Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
    color_palette = Blues8

    # Choose a title!
    title = 'Gene Network'

    # Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
        ("Character", "@index"),
        ("Degree", "@degree"),
        ("Modularity Class", "@modularity_class"),
        ("Modularity Color", "$color[swatch]:modularity_color"),
    ]

    # Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips=HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                  x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

    # Create a network graph object
    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
    network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

    # Set node sizes and colors according to node degree (color as category from attribute)
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)
    # Set node highlight colors
    network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                     line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                         line_width=2)

    # Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    # Set edge highlight colors
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

    # Highlight nodes and edges
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(network_graph)

    script, div = components(plot)
    save(plot, filename=f"./network/templates/network.html")
    return script, div


def node_list():
    node = network_dao.read_node_data()
    node = node['node_name']
    return node


def ego_graph(G, node_name):
    # df = network_dao.read_edge_data()
    # G = convert_to_G(df)
    return networkx.ego_graph(G, node_name)


def return_node_description(node_name):
    return NetworkNode.objects.filter(node_name__contains=node_name)

# Count some information in the node list,such as cancer driver
def neighbor_info_count(node_name):
    node_info = network_dao.get_node_by_name(node_name)
    node_neighbor = network_dao.get_neighbor_by_node_id(node_info.id)

    neighbor_count = {
        "average_degree",
        "essential_gene",
        "evolutionary_mouse",
        "evolutionary_fish",
        "evolutionary_fly",
        "evolutionary_worm",
        "evolutionary_yeast",
        "cell_signaling_signaling_protein",
        "cell_signaling_membrane_receptors",
        "cell_signaling_kinases",
        "cell_signaling_transcription_factors",
        "protein_abundance_high_copy_number",
        "protein_abundance_moderate_copy_number",
        "protein_adundance_low_copy_number",
        "protein_adundance_very_low_copy_number",
        "post_translational_modification_acetylation",
        "post_translational_modification_phosphorylation_ps_pt",
        "post_transaltional_modification_phosphorylation_py",
        "post_translational_modification_ubiquitination",
        "disease_genes_cancer_driver",
        "disease_genes_cancer1",
        "disease_genes_omim",
        "drug_target_therapeutic_targets",
        "drug_target_fda_approved",
        "drug_target_druggable",
        "regulators_of_cell_proliferation_go_genes",
        "regulatior_of_cell_proliferation_stop_genes",
        "immune_genes_core_ctl_genes",
        "immune_genes_car_genes",
        "immune_genes_checkpoint_genes"
    }

    return None