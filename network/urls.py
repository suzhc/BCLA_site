from django.contrib import admin
from django.urls import include, path
from network.views import home_page, return_node_page, return_all_node, return_node_description

urlpatterns = [
    path('<str:node_name>', return_node_page, name="return_node_page")
]