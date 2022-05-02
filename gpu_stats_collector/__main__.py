'''
Copyright (c) 2022, UC San Diego ITS/Educational Technology Services
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
'''

import time
import os
from .data_collection import create_gauge,start_server,process_request,data_publish


if __name__ == '__main__':
    #creating the guage for data publish
    gpu_metric = create_gauge()
    # starting the server
    start_server()
    
    while True:
        # poll the function to update the resourse information
        node_info = process_request()
        data_publish(node_info,gpu_metric)

        # wait till next polling
        time.sleep(5)

