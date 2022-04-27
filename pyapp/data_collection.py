import os
from .data_obj import Node
from prometheus_client import  Gauge, start_http_server
from kubernetes import client, config
from typing import Dict

# starting the server so that promethus can read the data
def start_server(port=8000)->None:
    '''
    create prometheus server with port number from env
    '''
    if "SEVERPORT" in os.environ:
        port  = int(os.getenv('SEVERPORT'))
    start_http_server(port)

def create_guage():
    '''
    create guage metric for gpu
    '''
    # creating the guage metric for promethus 
    # guage metric can increase and decrease check more on prometheus metric type
    gpu_metric = Gauge('dsmlp_gpu', 'Number of GPUS in use',['hostname','type','status','course'])
    return gpu_metric

def combine_node_pod_data(node_data,pod_data)->Dict:
    '''
    collects the total gpu resources from nodes
    collects the gpu being used from pod to map it to nodes
    '''
    # dict for storing all the nodes
    nodes={}
    for obj in node_data.items:
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

    # iterate over all the pods
    for obj in pod_data.items:
        
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


def process_request()->Dict:
    """
    Function to collect gpu usage data from the kubernetes nodes
    publish them on the server where prometheus can read 
    """
    # load the kubernetes configuration to execute the kubectl commands
    config.load_incluster_config()

    v1 = client.CoreV1Api()

    # collect all information for all nodes
    node_data = v1.list_node()
    

    # Retrive all the pod information to check the gpu request 
    pod_data = v1.list_pod_for_all_namespaces(watch=False)
    print(type(pod_data))
    # Breaking the functionality for testing pupose
    return combine_node_pod_data(node_data,pod_data)
    
    
   
def data_publish(nodes:Dict,gpu_metric)->None:
    '''
    used to publish the node information to server
    '''
    # publish the data in the form prometheus reads
    for _,node in nodes.items():
        # publish the data for total number of gpu present in the node
        gpu_metric.labels(node.node_label,node.gpu_type,'total', node.course_name).set(node.gpu_total)
        # publish the data for total number of gpu used in the node
        gpu_metric.labels(node.node_label,node.gpu_type,'reserved', node.course_name).set(node.gpu_used if node.gpu_used<= node.gpu_total else node.gpu_total)
        # publish the data for total number of gpu available in the node
        gpu_metric.labels(node.node_label,node.gpu_type,'available', node.course_name).set(node.gpu_total-node.gpu_used if 0<=(node.gpu_total-node.gpu_used) else 0)