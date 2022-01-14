from django.shortcuts import render_to_response
from scripts import script


# Create your views here.
def base_page(request):
    context = {}
    context['node_list'] = script.node_list()
    return render_to_response('base.html', context)

def all_node(request):
    df = script.read_the_csv()
    G = script.convert_to_G(df)
    script.draw_the_network(G)
    return render_to_response('network.html')

def node_page(request, node_name):
    df = script.read_the_csv()
    G = script.convert_to_G(df)
    G = script.ego_graph(G, node_name)
    script.draw_the_network(G)
    return render_to_response('network.html')

def node_description(request, node_name):
    pass