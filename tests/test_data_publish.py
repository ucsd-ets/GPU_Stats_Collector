import unittest
import requests
from pyapp import data_collection
from pyapp import data_obj

class TestDatapublish(unittest.TestCase):
    def setUp(self):
        # creating fake data
        node = data_obj.Node()
        node.course_name = 'test_course'
        node.node_label = 'test_node_name'
        node.gpu_type = '1080ti'
        node.gpu_used =1
        node.gpu_total=2
        self.data = {'test_node':node}
        # function to be tested
        self.data_publish = data_collection.data_publish
    
    def test_hello_world(self):
        # start the server 
        data_collection.start_server(9000)
        gpu_metric = data_collection.create_guage()
        # create the metric
        self.data_publish(nodes=self.data,gpu_metric=gpu_metric)
        # use http get method to read data
        r =requests.get('http://127.0.0.1:9000')
        # check the return data
        assert r.status_code == 200
        assert 'dsmlp_gpu{course="test_course",hostname="test_node_name",status="total",type="1080ti"} 2.0' in r.text
        assert 'dsmlp_gpu{course="test_course",hostname="test_node_name",status="reserved",type="1080ti"} 1.0' in r.text
        assert 'dsmlp_gpu{course="test_course",hostname="test_node_name",status="available",type="1080ti"} 1.0' in r.text