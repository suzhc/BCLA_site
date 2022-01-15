from django.contrib import admin
from .models import NodeDescription, Network
# Register your models here.


@admin.register(NodeDescription)
class NodeDescriptionAdmin(admin.ModelAdmin):
    list_display = ('node_name', 'node_description')


@admin.register(Network)
class Network(admin.ModelAdmin):
    list_display = ('Source', 'Target', 'Weight')