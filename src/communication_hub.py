import grpc

from src import util
from src import shared_variable_pb2_grpc as sv_grpc


class CommunicationHub:

    def __init__(self, node):
        self.node = node

    def get_stub_by_address(self, address):
        channel = grpc.insecure_channel(address.hostname + ":" + str(address.port))
        return sv_grpc.SharedVariableStub(channel)

    def get_next(self):
        return self.get_stub_by_address(self.node.next)

    def get_prev(self):
        return self.get_stub_by_address(self.node.prev)

    def get_nnext(self):
        return self.get_stub_by_address(self.node.nnext)

    def get_leader(self):
        return self.get_stub_by_address(self.node.leader)
