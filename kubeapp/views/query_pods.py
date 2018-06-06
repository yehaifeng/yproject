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
        pods_list = []
        config.load_kube_config(config_file='/home/oracle/.kube/config')
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
        for i in pods.items:
            pods_list.append({'ip':i.status.pod_ip, 'host_ip':i.status.host_ip, 'phase': i.status.phase, 'namespace':i.metadata.namespace, 'name':i.metadata.name})
        #data = json.dumps(pods_list)
        data = {'pods_list':pods_list}
        #return HttpResponse(data)
        return render(request, 'querypods.html', data)

    def post(self, request):
        req_dict = {}
        ret_data = []
        for key in request.POST:
            value = request.POST.getlist(key)[0]
            req_dict[key] = value
        print(req_dict)
        pods_list = []
        ns_list = []
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
