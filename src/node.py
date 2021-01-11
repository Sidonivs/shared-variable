import sys
import logging
import yaml
import time
import random
from concurrent import futures

import grpc

from src import shared_variable_pb2_grpc as sv_grpc
from src import shared_variable_pb2 as sv

from src import util
from src.shared_variable_servicer_impl import SharedVariableServicer
from src.communication_hub import CommunicationHub
from src.console_handler import ConsoleHandler

logging.basicConfig(level=logging.INFO)


class Node:
    this_node = None

    def __init__(self, config):
        # initial config
        self.id = config["id"]
        self.address = sv.Address(hostname=config["ip"], port=config["port"])
        self.otherNodeAddress = sv.Address(hostname=config["other_ip"], port=config["other_port"])

        # neighbours
        self.next = self.address
        self.prev = self.address
        self.nnext = self.address
        self.leader = self.address

        self.variable = ""
        self.timestamp = None

        self.repairing = False
        self.voting = False

        self.server = None
        self.hub = None
        self.cmd_handler = None

    def __str__(self):
        return f"Node[id: {self.id}, timestamp: {self.timestamp}, address: {util.address_to_string(self.address)} " \
               f"other_address: {util.address_to_string(self.otherNodeAddress)}]"

    def neighbours_to_string(self):
        return f"Neighbours[next - {self.next.hostname}:{self.next.port}, " \
               f"prev - {self.prev.hostname}:{self.prev.port}, " \
               f"nnext - {self.nnext.hostname}:{self.nnext.port}, " \
               f"leader - {self.leader.hostname}:{self.leader.port}]"

    def print_status(self):
        print(f"Status: {self} \nwith {self.neighbours_to_string()}")

    def generate_timestamp(self):
        timestamp = time.time()
        # makes sure timestamp is truly unique
        while timestamp == self.timestamp:
            time.sleep(0.1)
            timestamp = time.time()
        return timestamp

    def run(self):
        self.timestamp = self.generate_timestamp()
        self.print_status()

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        sv_grpc.add_SharedVariableServicer_to_server(SharedVariableServicer(self), self.server)
        self.server.add_insecure_port(self.address.hostname + ':' + str(self.address.port))
        # from doc: The server start() method is non-blocking. A new thread will be instantiated to handle requests.
        self.server.start()

        self.hub = CommunicationHub(self)

        # JOIN
        try:
            tmp_node = self.hub.get_stub_by_address(self.otherNodeAddress)
            join_reply = tmp_node.Join(sv.JoinReq(address=self.address))
            self.next = join_reply.next
            self.prev = join_reply.prev
            self.nnext = join_reply.nnext
            self.leader = join_reply.leader
        except grpc.RpcError as e:
            logging.error(msg="Join unsuccessful.", exc_info=e)
            self.stop(1)
        else:
            print(f"Join successful. \n{self.neighbours_to_string()}")

        self.cmd_handler = ConsoleHandler(self)
        self.cmd_handler.start()

    """ Can raise grpc.RpcError
    """
    def repair_topology(self, missing_address):
        counter = 0
        while self.repairing:
            if counter >= 100:
                raise grpc.RpcError("Waiting for another repair timed out.")

            print("Waiting for another repair...")
            time.sleep(random.randint(2, 5))
            counter += 1

        self.repairing = True

        my_servicer = self.hub.get_stub_by_address(self.address)
        my_servicer.NodeMissing(sv.NodeMissingMsg(address=missing_address))

        self.repairing = False
        print(f"Topology repaired. {self.neighbours_to_string()}")

    """ Can raise grpc.RpcError
    """
    def leader_election(self):
        try:
            self.hub.get_stub_by_address(self.address).Election(sv.ElectionMsg(timestamp=-1))
        except grpc.RpcError as e:
            logging.critical(msg="Leader election unsuccessful.", exc_info=e)
            raise e

    def read_shared_variable(self):
        if self.leader == self.address:
            # this node is the leader
            return self.hub.get_stub_by_address(self.address).ReadVar(sv.ReadVarReq()).variable

        read_successful = False
        counter = 0
        while not read_successful:
            if counter >= 10:
                raise grpc.RpcError("Reading shared variable timed out.")

            try:
                leader = self.hub.get_leader()
                read_var_reply = leader.ReadVar(sv.ReadVarReq())

                read_successful = True
                self.variable = read_var_reply.variable
                self.timestamp = read_var_reply.timestamp
                return self.variable

            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.FAILED_PRECONDITION:
                    logging.critical(e.details())
                    self.leader_election()
                else:
                    # print(e.code())
                    logging.warning(msg="Leader could not be reached.")
                    try:
                        self.repair_topology(self.leader)
                    except grpc.RpcError as e2:
                        logging.critical(msg="Repairing topology unsuccessful.", exc_info=e2)
                        raise e2

                    self.leader_election()
            counter += 1

    def write_to_shared_variable(self, value):
        if self.leader == self.address:
            # this node is the leader
            self.hub.get_stub_by_address(self.address).WriteVar(sv.WriteVarReq(variable=value))
            return

        write_successful = False
        counter = 0
        while not write_successful:
            if counter >= 10:
                raise grpc.RpcError("Writing to shared variable timed out.")

            try:
                leader = self.hub.get_leader()
                write_var_reply = leader.WriteVar(sv.WriteVarReq(variable=value))

                write_successful = True
                self.variable = value
                self.timestamp = write_var_reply.timestamp

            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.FAILED_PRECONDITION:
                    logging.critical(e.details())
                    self.leader_election()
                else:
                    logging.warning(msg="Leader could not be reached.", exc_info=e)
                    try:
                        self.repair_topology(self.leader)
                    except grpc.RpcError as e:
                        logging.critical(msg="Repairing topology unsuccessful.", exc_info=e)
                        raise e

                    self.leader_election()
            counter += 1

    def leave(self):
        if self.address == self.prev:
            # I am the only node
            return

        # TODO write my value to prev

        counter = 0
        while self.repairing:
            if counter >= 100:
                raise grpc.RpcError("Waiting for another repair timed out.")

            print("Waiting for another repair...")
            time.sleep(random.randint(2, 5))
            counter += 1

        self.repairing = True

        try:
            prev_node = self.hub.get_prev()
            prev_node.NodeMissing(sv.NodeMissingMsg(address=self.address))
        except grpc.RpcError as e:
            logging.error(msg="Failed to send leaving message.", exc_info=e)

        self.repairing = False

        if self.address == self.leader:
            self.leader_election()

    def stop(self, status, last_message=f"Node stopped."):
        print("Stopping server...")
        self.server.stop(4)
        print(last_message)
        sys.exit(status)

    def kill(self):
        self.stop(status=1)


def parse_args():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        logging.error(f"Program expects 1 argument (node id in node_config.yaml),"
                      f"\n{len(sys.argv) - 1} arguments given.")
        sys.exit(2)


def get_yaml_config(config_node_id):
    with open("../node_config.yaml", 'r') as stream:
        try:
            dictionary = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.exception(msg=f"Could not load yaml config.", exc_info=exc)
            sys.exit(2)

    config = dictionary[config_node_id]
    config["id"] = config_node_id
    return config


if __name__ == '__main__':
    config_node_id = parse_args()
    config = get_yaml_config(config_node_id)
    Node.this_node = Node(config)
    Node.this_node.run()
