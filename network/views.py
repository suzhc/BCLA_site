from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

import tkinter.messagebox
from tkinter import *

from django.contrib import messages

from .models import *

from scripts import script


# Create your views here.
def home_page(request):
    return render_to_response('home_page.html')


# 返回
def return_all_node(request):
    df = script.read_edge_data()
    G = script.convert_to_G(df)
    script.draw_the_network(G)
    return render_to_response('network.html')


# 此函数是用来返回节点自我中心网的可视化页面，后续须做到description页面里去
def return_node_page(request, node_name):
    df = script.read_edge_data()
    G = script.convert_to_G(df)
    G = script.ego_graph(G, node_name)
    script.draw_the_network(G)
    return render_to_response('network.html')

@csrf_exempt
def return_node_description(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        # 这里后改为自己写的函数，用来获取基因信息
        node_descriptions = NetworkNode.objects.filter(node_name__contains=searched).values()
        if len(node_descriptions) == 0:
            messages.error(request, 'There is no '+searched)
            return render(request, 'home_page.html')
        else:
            return render_to_response('description_page.html', {'searched': searched,
                                                                'node_descriptions': node_descriptions})
    else:
        return render_to_response('description_page.html')

