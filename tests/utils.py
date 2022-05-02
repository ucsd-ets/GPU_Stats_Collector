'''
Copyright (c) 2022, UC San Diego ITS/Educational Technology Services
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
'''

class Mockrequest():
    def __init__(self,gpu) -> None:
        self.requests = {'nvidia.com/gpu':str(gpu)}
class Mockcontainer():
    def __init__(self,gpus) -> None:
        self.resources = Mockrequest(gpus)
class Mockpod_spec():
    def __init__(self,node_name,gpus) -> None:
        self.node_name = node_name
        self.containers = [Mockcontainer(gpus)]


class Mockaddress():
    def __init__(self,nodename) -> None:
        self.type = 'Hostname'
        self.address = nodename

class Mocklabels():
    def __init__(self,gpu_type,course_name) -> None:
        self.labels = {'gputype':gpu_type,'course_name':course_name}

class Mockstatus():
    def __init__(self,nodename,gpus) -> None:
        self.addresses = [Mockaddress(nodename)] 
        self.allocatable = {'nvidia.com/gpu':str(gpus)}
        pass
class Node():
    def __init__(self,node_name,gpu_type,course_name,gpus,) -> None:
        self.metadata = Mocklabels(gpu_type,course_name)
        self.status = Mockstatus(node_name,gpus)
class Pod():
    def __init__(self,node_name,gpus) -> None:
        self.spec = Mockpod_spec(node_name,gpus)
class data():
    def __init__(self,data) -> None:
        self.items = [data]