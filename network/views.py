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

from scripts import script as util


# Create your views here.
def home_page(request):
    return render_to_response('home_page.html')


# 返回
def return_all_node(request):
    df = util.read_edge_data()
    G = util.convert_to_G(df)
    util.draw_the_network(G)
    return render_to_response('network.html')


# 此函数是用来返回节点自我中心网的可视化页面，后续须做到description页面里去
def return_node_page(request, node_name):

    df = util.read_edge_data()
    G = util.convert_to_G(df)
    G = util.ego_graph(G, node_name)
    util.draw_the_network(G)
    return render_to_response('network.html')


@csrf_exempt
def return_node_description(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        # 这里后改为自己写的函数，用来获取基因信息
        node_descriptions = NetworkNode.objects.filter(node_name=searched).values()
        df = pd.read_csv('node.csv')
        df.to_csv('new.csv')
        json_records = df.reset_index().to_json(orient='records')
        arr = json.loads(json_records)
        context = {'d': arr}
        if not len(node_descriptions):
            return redirect('home_page')
        else:
            df = util.read_edge_data()
            G = util.convert_to_G(df)
            G = util.ego_graph(G, searched)
            script, div = util.draw_the_network(G)
            return render_to_response('description_page.html', {'searched': searched,
                                                                'node_descriptions': node_descriptions,
                                                                'script': script,
                                                                'div': div,
                                                                'd': context})
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

