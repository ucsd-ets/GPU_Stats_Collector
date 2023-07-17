class Node():
    '''
    class to store the node properties 
    '''
    def __init__(self) -> None:
        '''
        node label: is used to store the node name
        gpu type: is used to store the gpu type eg 1080ti or 2080ti 
        course name: is used to associate the node with the course
        gpu used: gpu resource allocated
        gpu total: total gpu resource present in the node
        '''
        self.node_label = ''
        self.gpu_type = ''
        self.course_name = ''
        self.gpu_used=0
        self.gpu_total=0
