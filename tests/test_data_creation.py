from platform import node
import unittest
from pyapp import data_collection
from pyapp import data_obj
import yaml
import os
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
        self.prepare_data = data_collection.combine_node_pod_data
    
    def test_hello(self):
        nodes = self.prepare_data(self.node_data,self.pod_data)
        assert nodes[self.nodename].node_label == self.nodename
        assert nodes[self.nodename].course_name == self.coursename
        assert nodes[self.nodename].gpu_type == self.gpu_type
        assert nodes[self.nodename].gpu_total == self.gpus
        assert nodes[self.nodename].gpu_used == self.gpu_used
