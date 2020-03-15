
class dht:
    def __init__(self):
        self.id = 0
        self.ring_size = 0
        self.right_node = ""
        self.left_node = ""
    
    def get_id(self):
        return self.id
    def get_ring_size(self):
        return self.ring_size
    def get_right_node(self):
        return self.right_node
    def get_left_node(self):
        return self.left_node
    def set_right_node(self,node):
        self.right_node = node
    def set_left_node(self,node):
        self.left_node = node