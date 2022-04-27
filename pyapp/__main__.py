import time
import os
from .data_collection import create_guage,start_server,process_request,data_publish


if __name__ == '__main__':
    # run till infinity 
    print('created metric')
    gpu_metric = create_guage()
    print('creating server')
    start_server()
    print('stared server')
    while True:
        # poll the function to update the resourse information
        node_info = process_request()
        data_publish(node_info,gpu_metric)
        
        # wait till next polling
        time.sleep(5)

