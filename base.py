
class dht:
    def __init__(self):
        #dictionary for storing registered node objects
        self.reg_nodes = {}
        
        #list for storing nodes in dht
        self.dht_node = []

        #list for unavailable ports
        self.used_ports = []

        self.dht_completed = False

    def get_reg_nodes(self):
        return self.reg_nodes

    def get_dht_node(self):
        return self.dht_node

    def get_used_ports(self):
        return self.used_ports

    def get_dht_completed(self):
        return self.dht_completed

    def add_reg_nodes(self,username,node):
        self.reg_nodes[username] = node

    def add_dht_node(self,node):
        self.dht_node.append(node)

    def add_used_ports(self,port):
        self.used_ports.append(port)

    def set_dht_complete(self,state):
        self.dht_completed = state
