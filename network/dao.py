# -*- coding: utf-8 -*-
# @Time    : 2022/1/19 21:25
# @Author  : pcy
# @Site    : 
# @File    : dao.py
# @Software: PyCharm 
# @Comment : 数据库接口层，所有和models交互的函数需要放在这个层级中，views不直接和models交互

from .models import *
import pandas as pd

# demo function
def node_info_by_node_name(node_name):
    node_info = NetworkNode.objects.filter(node_name__contains=node_name).values()
    return node_info


def read_edge_data():
    G_df = pd.DataFrame(list(NetworkEdge.objects.all().values()))
    return G_df


def read_node_data():
    G_des = pd.DataFrame(list(NetworkNode.objects.all().values()))
    return G_des


def read_gene_node():
    gene_node = pd.read_csv('node.csv')
    return gene_node


def read_gene_edge():
    gene_edge = pd.read_csv('edge.csv')
    gene_edge = gene_edge.drop([0])
    gene_edge = gene_edge.drop(['Database'], axis=1)
    return gene_edge

# new function #

# get node info by node name
def get_node_by_name(node_name):
    node_info = BNetworkNode.objects.filter(name=node_name).values()
    return node_info


# get neighbor info by node id
def get_neighbor_by_node_id(node_id):
    neighbor = []
    target_neighbor = BNetworkEdge.objects.filter(source=node_id).values()
    source_neighbor = BNetworkEdge.objects.filter(target=node_id).values()
    neighbor.append(target_neighbor)
    neighbor.append(source_neighbor)
    return neighbor






# demo function #
def get_neighbor_node(node_name, edge_df):
    node_list = list(edge_df.loc[edge_df['Source'] == node_name]['Target'])
    node_list = node_list + list(edge_df.loc[edge_df['Target'] == node_name]['Source'])

    return  node_list





