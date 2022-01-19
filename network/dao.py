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

# neighbor




