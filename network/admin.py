from django.contrib import admin
from .models import NetworkNode, NetworkEdge
# Register your models here.


@admin.register(NetworkNode)
class NodeDescriptionAdmin(admin.ModelAdmin):
    list_display = ('node_name', 'node_description')


@admin.register(NetworkEdge)
class Network(admin.ModelAdmin):
    list_display = ('Source', 'Target', 'Weight')