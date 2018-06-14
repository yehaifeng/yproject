# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
import logging
import datetime

from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint
import json

logger = logging.getLogger('django')
# Create your views here.
class QueryPods(View):
    #v1 = client.CoreV1Api()
    def __init__(self):
        super(QueryPods, self).__init__()
        self.return_data = []
        self.v1 = client.CoreV1Api()

    def get(self, request):
        #pods_list = []
        #ns_list = []
        #req_dict = {}
        #for key in request.GET:
        #    value = request.GET.getlist(key)[0]
        #    req_dict[key] = value
        #print req_dict
        #pods = self.v1.list_pod_for_all_namespaces(watch=False)
        #for i in pods.items:
        #    pods_list.append({'ip':i.status.pod_ip, 'host_ip':i.status.host_ip, 'phase': i.status.phase, 'namespace':i.metadata.namespace, 'name':i.metadata.name})
        #namespaces = self.v1.list_namespace()
        #for ns in namespaces.items:
        #    ns_list.append(ns.metadata.name)
        #ret_dict = {'pods':pods_list, 'namespaces':ns_list }
        #ret_data = json.dumps(ret_dict)
        return render(request, 'querypods.html')

    def post(self, request):
        req_dict = {}
        pods_list = []
        ns_list = []
        method = None
        pod_name = None
        host_ip = None
        namespace = None
        #for key in request.POST:
        #    value = request.POST.getlist(key)[0]
        #    req_dict[key] = value
        pods = self.v1.list_pod_for_all_namespaces(watch=False)
        if request.body and request.body.strip() != '{}':
            req_dict = json.loads(request.body)
            method = req_dict['method'] if 'method' in req_dict and req_dict['method'].strip() != '' else 'query'
            pod_name = req_dict['pod_name'] if 'pod_name' in req_dict and req_dict['pod_name'].strip() != '' else None
            host_ip = req_dict['host_ip'] if 'host_ip' in req_dict and req_dict['host_ip'].strip() != '' else None
            namespace = req_dict['namespace'] if 'namespace' in req_dict and req_dict['namespace'].strip() != '' else None
            #logger.debug('3 var is: %(pod_name)s %(host_ip)s %(namespace)s', req_dict)
        for i in pods.items:
            if namespace or host_ip or pod_name:
                if namespace and namespace not in [i.metadata.namespace,'all']:
                    continue
                if host_ip and host_ip != i.status.host_ip:
                    continue
                if pod_name and pod_name not in i.metadata.name:
                    continue
            pods_list.append({'ip':i.status.pod_ip, 'host_ip':i.status.host_ip, 'phase': i.status.phase, 'namespace':i.metadata.namespace, 'name':i.metadata.name})
        if method and method == 'query':
            pass
        namespaces = self.v1.list_namespace()
        ns_list.append('all')
        for ns in namespaces.items:
            ns_list.append(ns.metadata.name)
        ret_dict = {'pods':pods_list, 'namespaces':ns_list }
        ret_data = json.dumps(ret_dict)
        return HttpResponse(ret_data)
