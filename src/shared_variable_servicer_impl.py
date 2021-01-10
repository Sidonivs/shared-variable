from src import shared_variable_pb2_grpc as sv_grpc
from src import shared_variable_pb2 as sv

from src import util


class SharedVariableServicer(sv_grpc.SharedVariableServicer):

    def __init__(self, node):
        self.node = node

    def Join(self, request, context):
        print("Join called.")
        reply = sv.JoinReply()

        if request.address == self.node.address:
            print("I am FIRST.")
            reply.next.CopyFrom(self.node.next)
            reply.prev.CopyFrom(self.node.prev)
            reply.nnext.CopyFrom(self.node.nnext)
            reply.leader.CopyFrom(self.node.leader)
        else:
            print(f"{util.address_to_string(request.address)} is joining.")

            # work around for only 2 nodes
            initial_next = sv.Address(hostname=self.node.next.hostname, port=self.node.next.port)
            initial_prev = sv.Address(hostname=self.node.prev.hostname, port=self.node.prev.port)

            reply.next.CopyFrom(self.node.next)
            reply.prev.CopyFrom(self.node.address)
            reply.nnext.CopyFrom(self.node.nnext)
            reply.leader.CopyFrom(self.node.leader)

            # send ChangePrev to (old) next node with new node address
            self.node.hub.get_next().ChangePrev(sv.ChangePrevMsg(prev=request.address))
            # send ChangeNNext to (old) prev node with new node address
            self.node.hub.get_stub_by_address(initial_prev).ChangeNNext(sv.ChangeNNextMsg(nnext=request.address))
            reply.nnext.CopyFrom(self.node.nnext)
            # edit my neighbours
            self.node.nnext = initial_next
            self.node.next = request.address

        return reply

    def ChangePrev(self, request, context):
        print("ChangePrev called.")
        self.node.prev = request.prev
        return self.node.next

    def ChangeNNext(self, request, context):
        print("ChangeNNext called.")
        self.node.nnext = request.nnext
        return sv.Ack(ack=True)

    def NodeMissing(self, request, context):
        print(f"NodeMissing called with {util.address_to_string(request.address)}.")
        self.node.repairing = True

        if request.address == self.node.next:
            self.node.next = self.node.nnext
            # send ChangePrev to nnext node with my address
            # nnext sends its next node to set as my new nnext
            self.node.nnext = self.node.hub.get_nnext().ChangePrev(sv.ChangePrevMsg(prev=self.node.address))
            # send ChangeNNext to prev node with my new next
            self.node.hub.get_prev().ChangeNNext(sv.ChangeNNextMsg(nnext=self.node.next))
            print("NodeMissing completed.")

        else:
            # send to next node to solve
            self.node.hub.get_next().NodeMissing(sv.NodeMissingMsg(address=request.address))

        self.node.repairing = False
        return sv.Ack(ack=True)

    def Election(self, request, context):
        pass

    def Elected(self, request, context):
        pass

    def ReadVar(self, request, context):
        if self.node.address != self.node.leader:
            # TODO fail
            pass

        timestamp = self.node.generate_timestamp()
        self.node.timestamp = timestamp
        print(f"[{timestamp}] Variable with value '{self.node.variable}' was read.")

        reply = sv.ReadVarReply()
        reply.variable = self.node.variable
        reply.timestamp = timestamp
        return reply

    def WriteVar(self, request, context):
        if self.node.address != self.node.leader:
            # TODO fail
            pass

        timestamp = self.node.generate_timestamp()
        self.node.timestamp = timestamp
        print(f"[{timestamp}] Writing to variable.")
        print(f"Old value: '{self.node.variable}'; New value: '{request.variable}'")

        self.node.variable = request.variable
        return sv.WriteVarReply(timestamp=timestamp)
