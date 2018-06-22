# coding: utf-8

from __future__ import absolute_import

from .index import index
from .obj_pod import QueryPods
from .rsc_node import QueryNodes
from .rsc_pv import QueryPv

from kubernetes import client, config

config.load_kube_config(config_file='/home/oracle/.kube/config')
