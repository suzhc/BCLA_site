from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class NodeDescription(models.Model):
    node_name = models.CharField(max_length=15)
    node_description = models.TextField()

    def __str__(self):
        return self.node_name


class Network(models.Model):
    Source = models.ForeignKey(NodeDescription, related_name='source', on_delete=models.DO_NOTHING)
    Target = models.ForeignKey(NodeDescription, related_name='Target', on_delete=models.DO_NOTHING)
    Weight = models.IntegerField()

    def __str__(self):
        return self.Source.node_name + "->" + self.Target.node_name
