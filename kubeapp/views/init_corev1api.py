#!/usr/bin/env python
# coding: utf-8

from from kubernetes.client.rest import ApiException
from kubernetes import client, config
# from pprint import pprint
# import json

class KubeCoreV1Api():
    def __init__(self, config=None, apiserver=None):
        config.load_kube_config(config_file='/home/oracle/.kube/config')
        v1 = client.CoreV1Api()
