import logging
import grpc

from src import shared_variable_pb2_grpc as sv_grpc
from src import shared_variable_pb2 as sv

from src import util


class SharedVariableServicer(sv_grpc.SharedVariableServicer):

    def __init__(self, node):
        self.node = node

    def Join(self, request, context):
        print("Join called.")
        reply = sv.JoinReply()

        self.node.wait_for_repair()
        self.node.repairing = True

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

        self.node.repairing = False
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

            if self.node.address == self.node.leader:
                # my backup just died, make a new one
                self.node.backup_variable()

        else:
            # send to next node to solve
            self.node.hub.get_next().NodeMissing(sv.NodeMissingMsg(address=request.address))

        self.node.repairing = False
        return sv.Ack(ack=True)

    def CheckNodes(self, request, context):
        print("CheckNodes called.")

        if self.node.check_nodes_author and request.stop:
            self.node.check_nodes_author = False
            print("CheckNodes completed.")
            return sv.Ack(ack=True)

        self.node.wait_for_repair()

        check_nodes_success = False
        while not check_nodes_success:
            try:
                self.node.hub.get_next().CheckNodes(sv.CheckNodesMsg(stop=True))
                check_nodes_success = True
            except grpc.RpcError as e:
                logging.warning(f"Next node for CheckNodes message could not be reached: {e.code()}.")
                self.node.repair_topology(self.node.next)

        return sv.Ack(ack=True)

    def Election(self, request, context):
        print(f"Election called with timestamp [{request.timestamp}]")

        self.node.wait_for_repair()

        if self.node.timestamp < request.timestamp:
            self.node.voting = True

            election_send_success = False
            while not election_send_success:
                try:
                    self.node.hub.get_next().Election(sv.ElectionMsg(timestamp=request.timestamp))
                    election_send_success = True
                except grpc.RpcError as e:
                    logging.warning(f"Next node for the Election message could not be reached: {e.code()}.")
                    self.node.repair_topology(self.node.next)

        elif self.node.timestamp > request.timestamp and not self.node.voting:
            self.node.voting = True

            election_send_success = False
            while not election_send_success:
                try:
                    self.node.hub.get_next().Election(sv.ElectionMsg(timestamp=self.node.timestamp))
                    election_send_success = True
                except grpc.RpcError as e:
                    logging.warning(f"Next node for the Election message could not be reached: {e.code()}.")
                    self.node.repair_topology(self.node.next)

        elif self.node.timestamp == request.timestamp:
            # I am leader, sending elected message
            elected_send_success = False
            while not elected_send_success:
                try:
                    self.node.hub.get_next().Elected(sv.ElectedMsg(leader=self.node.address, timestamp=self.node.timestamp))
                    elected_send_success = True
                except grpc.RpcError as e:
                    logging.warning(f"Next node for the Elected message could not be reached: {e.code()}.")
                    self.node.repair_topology(self.node.next)

        return sv.Ack(ack=True)

    def Elected(self, request, context):
        print(f"Elected called with leader [{util.address_to_string(request.leader)}] and timestamp [{request.timestamp}]")
        self.node.wait_for_repair()

        self.node.leader = request.leader
        self.node.voting = False

        if self.node.address != request.leader:
            elected_send_success = False
            while not elected_send_success:
                try:
                    self.node.hub.get_next().Elected(sv.ElectedMsg(leader=request.leader, timestamp=request.timestamp))
                    elected_send_success = True
                except grpc.RpcError as e:
                    logging.warning(f"Next node for the Elected message could not be reached: {e.code()}.")
                    self.node.repair_topology(self.node.next)
        else:
            # the new leader makes a backup of the variable in the next node
            self.node.backup_variable()

        return sv.Ack(ack=True)

    def ReadVar(self, request, context):
        if self.node.address != self.node.leader:
            logging.critical("Trying to read from a node that is not the leader!")
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Trying to read from a node that is not the leader!")

        timestamp = self.node.generate_timestamp()
        self.node.timestamp = timestamp
        print(f"[{timestamp}] Variable with value '{self.node.variable}' was read.")

        reply = sv.ReadVarReply()
        reply.variable = self.node.variable
        reply.timestamp = timestamp
        return reply

    def WriteVar(self, request, context):
        timestamp = self.node.generate_timestamp()
        self.node.timestamp = timestamp
        print(f"[{timestamp}] Writing to variable.")
        print(f"Old value: '{self.node.variable}'; New value: '{request.variable}'")

        self.node.variable = request.variable

        return sv.WriteVarReply(timestamp=timestamp)
