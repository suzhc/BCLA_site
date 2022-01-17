from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import *

from scripts import script


# Create your views here.
def home_page(request):
    context = {}
    context['node_list'] = script.node_list()
    return render_to_response('home_page.html', context)


def return_all_node(request):
    df = script.read_edge_data()
    G = script.convert_to_G(df)
    script.draw_the_network(G)
    return render_to_response('network.html')


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
        node_descriptions = NetworkNode.objects.filter(node_name__contains=searched).values()
        return render_to_response('description_page.html', {'searched': searched,
                                                            'node_descriptions': node_descriptions})
    else:
        return render_to_response('description_page.html', )

