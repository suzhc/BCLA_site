import json
import os
import mimetypes

from django.shortcuts import render_to_response, render, redirect, reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.http.response import HttpResponse

import pandas as pd

from .models import *

import network.dao as network_dao
import network.tools as network_tools


# Create your views here.
@csrf_exempt
def home_page(request):
    # 搜索后
    if request.method == 'POST':
        context = {}
        searched = request.POST['searched']
        # # 这里后改为自己写的函数，用来获取基因信息
        # df_edge = network_dao.read_gene_edge()
        # df_node = network_dao.read_gene_node()
        # node_descriptions = df_node[df_node.Gene == searched]
        # # node_descriptions = list(node_descriptions)
        # json_records = df_node.reset_index().to_json(orient='records')
        # arr = json.loads(json_records)
        # table = {'d': arr}
        # neighbor_nodes = network_dao.get_neighbor_node(searched, df_edge)
        # neighbor_nodes = df_node.query("Gene == @neighbor_nodes")
        # G = network_tools.convert_to_G(df_edge)
        # G = network_tools.ego_graph(G, searched)
        # script, div = network_tools.draw_the_network(G)
        # context["searched"] = searched
        # context["script"] = script
        # context["div"] = div

        try:
            # 获取被搜索基因的信息
            gene_info = network_dao.get_node_by_name(searched)
            # 获取被搜索基因邻居节点的信息
            neigbor_info = network_dao.get_neighbor_by_node_id(gene_info.id)
            neigbor_info = pd.DataFrame(neigbor_info)
            # 获取自我中心网
            G = network_tools.convert_to_G(network_dao.get_all_edge())
            G = network_tools.ego_graph(G, gene_info.id)
            script, div = network_tools.draw_the_network(G)
            ego_graph = {'script': script, 'div': div}

            context["gene_info"] = gene_info
            context["neigbor_info"] = neigbor_info
            context["ego_graph"] = ego_graph

            return render_to_response('main.html', context)
        except:
            return render_to_response('main.html', {'searched': searched})

    # 未搜索
    else:
        return render_to_response('main.html')


# 返回
def return_all_node(request):
    df = network_dao.read_edge_data()
    G = network_tools.convert_to_G(df)
    network_tools.draw_the_network(G)
    return render_to_response('network.html')


# 此函数是用来返回节点自我中心网的可视化页面，后续须做到description页面里去
def return_node_page(request, node_name):
    df = network_dao.read_edge_data()
    G = network_tools.convert_to_G(df)
    G = network_tools.ego_graph(G, node_name)
    network_tools.draw_the_network(G)
    return render_to_response('network.html')


@csrf_exempt
def return_node_description(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        # 这里后改为自己写的函数，用来获取基因信息
        df_edge = network_dao.read_gene_edge()
        df_node = network_dao.read_gene_node()
        node_descriptions = df_node[df_node.Gene == searched]
        # node_descriptions = list(node_descriptions)
        json_records = df_node.reset_index().to_json(orient='records')
        arr = json.loads(json_records)
        context = {'d': arr}
        neighbor_nodes = network_dao.get_neighbor_node(searched, df_edge)
        neighbor_nodes = df_node.query("Gene == @neighbor_nodes")
        G = network_tools.convert_to_G(df_edge)
        try:
            G = network_tools.ego_graph(G, searched)
            script, div = network_tools.draw_the_network(G)
            return render_to_response('description_page.html', {'searched': searched,
                                                                'node_descriptions': node_descriptions,
                                                                'neighbor_nodes': neighbor_nodes,
                                                                'script': script,
                                                                'div': div,
                                                                'd': context})

        except:
            return redirect('home_page')

    else:
        return render_to_response('description_page.html')


def download_file(request):
    filename = 'new.csv'
    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
