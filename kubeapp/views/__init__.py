# coding: utf-8

from __future__ import absolute_import

from .index import index
from .query_pods import QueryPods
from .query_nodes import QueryNodes

from kubernetes import client, config

config.load_kube_config(config_file='/home/oracle/.kube/config')
