# -*- coding: utf-8 -*-
# @Time    : 2022/1/19 21:25
# @Author  : pcy
# @Site    : 
# @File    : dao.py
# @Software: PyCharm 
# @Comment : 数据库接口层，所有和models交互的函数需要放在这个层级中，views不直接和models交互
from django.db.models import Q
from django.forms.models import model_to_dict

import network.models as network_models
import pandas as pd

# demo function
def node_info_by_node_name(node_name):
    node_info = network_models.NetworkNode.objects.filter(node_name__contains=node_name).values()
    return node_info


def read_edge_data():
    G_df = pd.DataFrame(list(network_models.NetworkEdge.objects.all().values()))
    return G_df


def read_node_data():
    G_des = pd.DataFrame(list(network_models.NetworkNode.objects.all().values()))
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
    node_info = network_models.BNetworkNode.objects.filter(name=node_name)[0]
    return node_info

# get node info by node id
def get_node_by_id(node_id):
    node_info = network_models.BNetworkNode.objects.filter(id=node_id)[0]
    return node_info

# get neighbor edge by node id
def get_edge_by_node_id(node_id):
    target_neighbor = network_models.BNetworkEdge.objects.filter(Q(source=node_id) | Q(target=node_id))
    # source_neighbor = network_models.BNetworkEdge.objects.filter(target=node_id)
    # neighbor_edge = target_neighbor.extend(source_neighbor)
    return target_neighbor

# get neighbor node by node id
def get_neighbor_by_node_id(node_id):
    node_list = []
    neighbor_edge =get_edge_by_node_id(node_id)
    for temp_edge in neighbor_edge:
        temp_node_info = get_node_by_id(temp_edge.source)
        temp_node_info = model_to_dict(temp_node_info)
        node_list.append(temp_node_info)
        temp_node_info = get_node_by_id(temp_edge.target)
        temp_node_info = model_to_dict(temp_node_info)
        node_list.append(temp_node_info)
    return node_list

# 获取全网
def get_all_edge():
    return network_models.BNetworkEdge.objects.filter()






