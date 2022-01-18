from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(NetworkNode)
class NodeDescriptionAdmin(admin.ModelAdmin):
    list_display = ('node_name', 'node_description')


@admin.register(NetworkEdge)
class Network(admin.ModelAdmin):
    list_display = ('Source', 'Target', 'Weight')


@admin.register(BNetworkEdge)
class BNetworkEdge(admin.ModelAdmin):
    list_display = ('source', 'target')


@admin.register(BNetworkNode)
class BNetworkNode(admin.ModelAdmin):
    list_display = ('name', 'degree')