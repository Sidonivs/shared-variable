import grpc

from src import util
from src import shared_variable_pb2_grpc as sv_grpc


class CommunicationHub:

    def __init__(self, node):
        self.node = node
        self.stubs = {}

    def remove_stub(self, address):
        if util.address_to_string(address) in self.stubs:
            del self.stubs[util.address_to_string(address)]

    def reset_stubs(self):
        self.stubs = {}

    def get_stub_by_address(self, address):
        addr_str = util.address_to_string(address)
        if addr_str in self.stubs:
            stub = self.stubs[addr_str]
        else:
            channel = grpc.insecure_channel(addr_str)
            stub = sv_grpc.SharedVariableStub(channel)
            self.stubs[addr_str] = stub

        return stub

    def get_next(self):
        return self.get_stub_by_address(self.node.next)

    def get_prev(self):
        return self.get_stub_by_address(self.node.prev)

    def get_nnext(self):
        return self.get_stub_by_address(self.node.nnext)

    def get_leader(self):
        return self.get_stub_by_address(self.node.leader)
