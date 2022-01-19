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
def home_page(request):
    return render_to_response('home_page.html')


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
        node_descriptions = list(node_descriptions)
        json_records = df_node.reset_index().to_json(orient='records')
        arr = json.loads(json_records)
        context = {'d': arr}
        G = network_tools.convert_to_G(df_edge)
        try:
            G = network_tools.ego_graph(G, searched)
            script, div = network_tools.draw_the_network(G)
            return render_to_response('description_page.html', {'searched': searched,
                                                                'node_descriptions': node_descriptions,
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
