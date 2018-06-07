# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
import datetime

from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint
import json

# Create your views here.
class QueryPods(View):
    def __init__(self):
        self.return_data = []

    def get(self, request):
        #pods_list = []
        #config.load_kube_config(config_file='/home/oracle/.kube/config')
        #v1 = client.CoreV1Api()
        #pods = v1.list_pod_for_all_namespaces(watch=False)
        #for i in pods.items:
        #    pods_list.append({'ip':i.status.pod_ip, 'host_ip':i.status.host_ip, 'phase': i.status.phase, 'namespace':i.metadata.namespace, 'name':i.metadata.name})
        #data = {'pods_list':pods_list}
        return render(request, 'querypods.html')

    def post(self, request):
        req_dict = {}
        pods_list = []
        ns_list = []
        #for key in request.POST:
        #    value = request.POST.getlist(key)[0]
        #    req_dict[key] = value
        if request.body:
            req_dict = json.loads(request.body)
            pod_name = req_dict['pod_name'] if 'pod_name' in req_dict and req_dict['pod_name'] != '' else None
            host_ip = req_dict['host_ip'] if 'host_ip' in req_dict and req_dict['host_ip'] != '' else None
            namespace = req_dict['namespace'] if 'namespace' in req_dict and req_dict['namespace'] != '' else None
            print pod_name, host_ip, namespace
        config.load_kube_config(config_file='/home/oracle/.kube/config')
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
        for i in pods.items:
            pods_list.append({'ip':i.status.pod_ip, 'host_ip':i.status.host_ip, 'phase': i.status.phase, 'namespace':i.metadata.namespace, 'name':i.metadata.name})
        namespaces = v1.list_namespace()
        for ns in namespaces.items:
            ns_list.append(ns.metadata.name)
        ret_dict = {'pods':pods_list, 'namespaces':ns_list }
        ret_data = json.dumps(ret_dict)
        return HttpResponse(ret_data)
