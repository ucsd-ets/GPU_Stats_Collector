import time
import os
from .data_obj import Node
from prometheus_client import  Gauge, start_http_server
from kubernetes import client, config
from typing import Dict


# load the kubernetes configuration to execute the kubectl commands
config.load_incluster_config()

# starting the server so that promethus can read the data
port=8000
if "SEVERPORT" in os.environ:
    port  = int(os.getenv('SEVERPORT'))
start_http_server(port)

# creating the guage metric for promethus 
# guage metric can increase and decrease check more on prometheus metric type
ti_1080 = Gauge('dsmlp_gpu', 'Number of GPUS in use',['hostname','type','status','course'])


def process_request()->Dict:
    """
    Function to collect gpu usage data from the kubernetes nodes
    publish them on the server where prometheus can read 
    """
    v1 = client.CoreV1Api()
    # collect all information for all nodes
    ret = v1.list_node()
    # dict for storing all the nodes
    nodes={}
    for obj in ret.items:
        # iterating over all the nodes
        node = Node()
        # check if the node has gpu from the label if not then move to next node
        if 'gputype' in obj.metadata.labels:
            node.gpu_type = obj.metadata.labels['gputype']
        else:
            continue
        # Extract the node label from the address when type is hostname 
        for address_node in obj.status.addresses: 
            if address_node.type == 'Hostname':
                node.node_label = address_node.address
        # Extract the course information for the node from the labels
        if 'course_name' in obj.metadata.labels:
            node.course_name = obj.metadata.labels['course_name']
        
        # total gpu in the node is present in allocatable 
        node.gpu_total = int(obj.status.allocatable['nvidia.com/gpu'])
        
        # store the node in the dict for checking the gpus in use
        nodes[node.node_label]=node
        
    # Retrive all the pod information to check the gpu request 
    ret = v1.list_pod_for_all_namespaces(watch=False)
    
    # iterate over all the pods
    for obj in ret.items:
        # if pod is associated with any node with gpu then go ahead or continue to next pod
        if obj.spec.node_name is None:
            continue
        node_label = obj.spec.node_name
        # if node name not in dict move on
        if node_label not in nodes:
            continue
        if obj.spec.containers[0].resources.requests is None:
            continue
        # extract the gpu request of the pod 
        if 'nvidia.com/gpu' in obj.spec.containers[0].resources.requests:
            nodes[node_label].gpu_used += int(obj.spec.containers[0].resources.requests['nvidia.com/gpu'])
    return nodes
   
def data_publish(nodes:Dict)->None:
    '''
    used to publish the node information to server
    '''
    # publish the data in the form prometheus reads
    for node_name,node in nodes.items():
        # publish the data for total number of gpu present in the node
        ti_1080.labels(node.node_label,node.gpu_type,'total', node.course_name).set(node.gpu_total)
        # publish the data for total number of gpu used in the node
        ti_1080.labels(node.node_label,node.gpu_type,'reserved', node.course_name).set(node.gpu_used if node.gpu_used<= node.gpu_total else node.gpu_total)
        # publish the data for total number of gpu available in the node
        ti_1080.labels(node.node_label,node.gpu_type,'available', node.course_name).set(node.gpu_total-node.gpu_used if 0<=(node.gpu_total-node.gpu_used) else 0)

if __name__ == '__main__':
    # run till infinity 
    while True:
        # poll the function to update the resourse information
        node_info = process_request()
        data_publish(node_info)
        # wait till next polling
        time.sleep(5)

