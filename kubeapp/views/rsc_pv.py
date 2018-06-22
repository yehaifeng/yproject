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
class QueryPv(View):
    def __init__(self):
        super(QueryPv, self).__init__()
        self.return_data = []
        self.v1 = client.CoreV1Api()

    def get(self, request):
        return render(request, 'querypv.html')

    def post(self, request):
        req_dict = {}
        ret_list = []
        ns_list = []
        method = None
        name = None
        
        pvs = self.v1.list_persistent_volume(watch=False)
        print type(pvs)
        if request.body and request.body.strip() != '{}':
            req_dict = json.loads(request.body)
            method = req_dict['method'] if 'method' in req_dict and req_dict['method'].strip() != '' else 'query'
            name = req_dict['name'] if 'name' in req_dict and req_dict['name'].strip() != '' else None
            #label = req_dict['label'] if 'label' in req_dict and req_dict['label'].strip() != '' else None
            #status = req_dict['status'].lower() if 'status' in req_dict and req_dict['status'].strip() != '' else None
            #logger.debug('3 var is: %(pod_name)s %(host_ip)s %(namespace)s', req_dict)
        for i in pvs.items:
            if name and name not in i.metadata.name:
                continue
            ret_name = i.metadata.name
            ret_status = i.status.phase
            ret_capacity = i.spec.capacity['storage']
            ret_mode = i.spec.access_modes
            ret_claimref = i.spec.claim_ref.name
            
            ret_list.append({'field1': ret_name, 'field2': ret_capacity, 'field3': ret_mode, 'field4': ret_claimref, 'field5': ret_status})
        if method and method == 'query':
            pass
        ret_title = ('name', 'capacity', 'access_mode', 'claimref', 'status')
        ret_dict = {'items': ret_list, 'title': ret_title, 'detail_data': pvs}
        ret_data = json.dumps(ret_dict)
        return HttpResponse(ret_data)
