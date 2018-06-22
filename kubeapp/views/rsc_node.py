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
class QueryNodes(View):
    def __init__(self):
        super(QueryNodes, self).__init__()
        self.return_data = []
        self.v1 = client.CoreV1Api()

    def get(self, request):
        return render(request, 'querynodes.html')

    def post(self, request):
        req_dict = {}
        ret_list = []
        ns_list = []
        method = None
        node_name = None
        label = None
        status = None
        #for key in request.POST:
        #    value = request.POST.getlist(key)[0]
        #    req_dict[key] = value
        nodes = self.v1.list_node(watch=False)
        if request.body and request.body.strip() != '{}':
            req_dict = json.loads(request.body)
            method = req_dict['method'] if 'method' in req_dict and req_dict['method'].strip() != '' else 'query'
            node_name = req_dict['node_name'] if 'node_name' in req_dict and req_dict['node_name'].strip() != '' else None
            label = req_dict['label'] if 'label' in req_dict and req_dict['label'].strip() != '' else None
            status = req_dict['status'].lower() if 'status' in req_dict and req_dict['status'].strip() != '' else None
            #logger.debug('3 var is: %(pod_name)s %(host_ip)s %(namespace)s', req_dict)
        for i in nodes.items:
            label_flag = 0
            if node_name or label or status:
                if status and status not in [i.status.conditions[-1].type.lower(),'all']:
                    continue
                if node_name and node_name != i.status.addresses[1].address:
                    continue
                if label:
                    for lk,lv in i.metadata.labels.items():
                        if label in lk or label in lv:
                            label_flag += 1
            if label and label_flag == 0:
                continue
            ret_node_name = i.status.addresses[1].address
            ret_status = i.status.conditions[-1].type
            ret_labels_dict = i.metadata.labels
            ret_roles = []
            ret_labels = []
            ret_version = i.status.node_info.kubelet_version
            for k,v in ret_labels_dict.items():
                if k.split('/')[0] == 'node-role.kubernetes.io':
                    ret_roles.append(k.split('/')[1].split(':')[0])
                ret_labels.append({'name':k, 'value':v})
            ret_list.append({'node_name': ret_node_name, 'status': ret_status, 'roles': ret_roles, 'version': ret_version, 'labels': ret_labels})
        if method and method == 'query':
            pass
        ret_title = ('node_name', 'status', 'roles', 'version', 'labels')
        ret_dict = {'items': ret_list, 'title': ret_title}
        ret_data = json.dumps(ret_dict)
        return HttpResponse(ret_data)
