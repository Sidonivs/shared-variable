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
        return f"Node[id: {self.id}, IP: {self.address.hostname}, port: {self.address.port}, " \
               f"otherIP: {self.otherNodeAddress.hostname}, otherPort: {self.otherNodeAddress.port}]"

    def neighbours_to_string(self):
        return f"Neighbours[next - {self.next.hostname}:{self.next.port}, " \
               f"prev - {self.prev.hostname}:{self.prev.port}, " \
               f"nnext - {self.nnext.hostname}:{self.nnext.port}, " \
               f"leader - {self.leader.hostname}:{self.leader.port}]"

    def print_status(self):
        print(f"Status: {self} \nwith {self.neighbours_to_string()}")

    def generate_timestamp(self):
        return str(time.time())

    def run(self):
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
        while self.repairing:
            print("Waiting for another repair...")
            time.sleep(random.randint(3, 6))

        self.repairing = True

        my_servicer = self.hub.get_stub_by_address(self.address)
        my_servicer.NodeMissing(sv.NodeMissingMsg(address=missing_address))

        self.repairing = False

    def read_shared_variable(self):
        if self.leader == self.address:
            # this node is the leader
            return self.hub.get_stub_by_address(self.address).ReadVar(sv.ReadVarReq()).variable

        read_successful = False
        while not read_successful:
            try:
                leader = self.hub.get_leader()
                read_var_reply = leader.ReadVar(sv.ReadVarReq())

                read_successful = True
                self.variable = read_var_reply.variable
                self.timestamp = read_var_reply.timestamp
                return self.variable

            except grpc.RpcError as e:
                logging.warning(msg="Leader could not be reached.")
                try:
                    self.repair_topology(self.leader)
                    return "LE"
                    # TODO LE
                except grpc.RpcError as e:
                    logging.error(msg="Repairing topology unsuccessful.", exc_info=e)
                    raise e

    def write_to_shared_variable(self, value):
        if self.leader == self.address:
            # this node is the leader
            self.hub.get_stub_by_address(self.address).WriteVar(sv.WriteVarReq(variable=value))
            return

        write_successful = False
        while not write_successful:
            try:
                leader = self.hub.get_leader()
                write_var_reply = leader.WriteVar(sv.WriteVarReq(variable=value))

                write_successful = True
                self.variable = value
                self.timestamp = write_var_reply.timestamp

            except grpc.RpcError as e:
                logging.warning(msg="Leader could not be reached.", exc_info=e)
                try:
                    self.repair_topology(self.leader)
                    return
                    # TODO LE
                except grpc.RpcError as e:
                    logging.error(msg="Repairing topology unsuccessful.", exc_info=e)
                    raise e

    def leave(self):
        while self.repairing:
            print("Waiting for another repair...")
            time.sleep(5)

        self.repairing = True

        try:
            prev_node = self.hub.get_prev()
            prev_node.NodeMissing(sv.NodeMissingMsg(address=self.address))
        except grpc.RpcError as e:
            logging.error(msg="Failed to send leaving message.", exc_info=e)

        self.repairing = False

    def stop(self, status):
        print("Stopping server...")
        self.server.stop(3)
        print(f"{self} stopped.")
        sys.exit(status)


def parse_args():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        logging.error(f"Program expects 1 argument (node id in node_config.yaml),\n{len(sys.argv)} arguments given.")
        sys.exit(2)


def get_yaml_config(config_node_id):
    # dictionary = {}
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