'''
Copyright (c) 2022, UC San Diego ITS/Educational Technology Services
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
'''
from platform import node
import unittest
from gpu_stats_collector import data_collection
from .utils import data,Node,Pod 
class TestNode(unittest.TestCase):
    def setUp(self):
        self.nodename = 'its-dsmlp-n01.ucsd.edu'
        self.coursename = 'test'
        self.gpu_type = 'ti1080'
        self.gpus =2
        self.gpu_used = 1
        self.node_data = data(Node(self.nodename,self.gpu_type,self.coursename,self.gpus))
        self.pod_data = data(Pod(self.nodename,self.gpu_used))
        self.prepare_data = data_collection.build_nodes
    
    def test_data_preparation(self):
        nodes = self.prepare_data(self.node_data,self.pod_data)
        assert nodes[self.nodename].node_label == self.nodename
        assert nodes[self.nodename].course_name == self.coursename
        assert nodes[self.nodename].gpu_type == self.gpu_type
        assert nodes[self.nodename].gpu_total == self.gpus
        assert nodes[self.nodename].gpu_used == self.gpu_used
