
class dht:
    def __init__(self):
        self.id = 0
        self.ip = ""
        self.port = ""
        self.ring_size = 0
        self.right_node = ""
        self.left_node = ""
    
    def get_id(self):
        return self.id

    def get_ring_size(self):
        return self.ring_size

    def get_right_node(self):
        return self.right_node

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_left_node(self):
        return self.left_node

    def set_id(self,id):
        self.id = id

    def set_ip(self,ip):
        self.ip = ip

    def set_port(self,port):
        self.port = port

    def set_ring_size(self,ring):
        self.ring_size = ring

    def set_right_node(self,node):
        self.right_node = node

    def set_left_node(self,node):
        self.left_node = node
