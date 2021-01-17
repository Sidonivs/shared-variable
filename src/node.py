import sys
import logging
import yaml
import time
from concurrent import futures
import threading

import grpc

from src import shared_variable_pb2_grpc as sv_grpc
from src import shared_variable_pb2 as sv

from src import util
from src.shared_variable_servicer_impl import SharedVariableServicer
from src.communication_hub import CommunicationHub
from src.console_handler import ConsoleHandler


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

        self.repairing_cv = threading.Condition()
        self.repairing = False
        self.writing_cv = threading.Condition()
        self.writing = False
        self.voting = False

        self.missing_address = None
        self.check_nodes_author = False

        self.server = None
        self.hub = None
        self.cmd_handler = None

    def __str__(self):
        return f"Node[id: {self.id}, variable: {self.variable}, timestamp: {self.timestamp}, " \
               f"address: {util.address_to_string(self.address)} " \
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

        # first read
        try:
            self.read_shared_variable()
        except grpc.RpcError as e:
            logging.error(msg="First read unsuccessful.", exc_info=e)
            self.leave()
            self.stop(1)

        self.cmd_handler = ConsoleHandler(self)
        self.cmd_handler.start()

    def wait_for_repair(self):
        with self.repairing_cv:
            self.repairing_cv.wait_for(lambda: not self.repairing)

    """ Can raise TimeoutError or grpc.RpcError
    """
    def repair_topology(self, missing_address):
        try:
            my_servicer = self.hub.get_stub_by_address(self.address)
            my_servicer.NodeMissing(sv.NodeMissingMsg(address=missing_address))
        except grpc.RpcError as e:
            logging.critical(msg="Topology repair unsuccessful. (Another node disconnected.)", exc_info=e)

        print(f"Topology repaired. {self.neighbours_to_string()}")

        if missing_address == self.leader:
            self.leader_election()

    """ Can raise grpc.RpcError
    """
    def leader_election(self):
        try:
            self.hub.get_stub_by_address(self.address).Election(sv.ElectionMsg(timestamp=-1))
        except grpc.RpcError as e:
            logging.critical(msg="Leader election unsuccessful.", exc_info=e)
            raise e

    def check_topology(self):
        self.check_nodes_author = True

        try:
            self.hub.get_stub_by_address(self.address).CheckNodes(sv.CheckNodesMsg(stop=False))
        except grpc.RpcError as e:
            logging.critical(msg="Could not start checking topology.", exc_info=e)
            raise e

    def read_shared_variable(self):
        self.wait_for_repair()

        read_successful = False
        counter = 0
        while not read_successful:
            if counter >= 20:
                raise TimeoutError("Reading shared variable timed out.")

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
                    # this node's leader does not think he is leader, attempt to fix this by electing a new one
                    self.leader_election()
                else:
                    logging.warning(msg=f"Leader could not be reached: {e.code()}.")

                    self.repair_topology(self.leader)

            counter += 1

    def write_to_shared_variable(self, value):
        self.wait_for_repair()

        write_successful = False
        counter = 0
        while not write_successful:
            if counter >= 20:
                raise TimeoutError("Writing to shared variable timed out.")

            try:
                leader = self.hub.get_leader()
                write_var_reply = leader.WriteVar(sv.WriteVarReq(variable=value))

                write_successful = True
                self.variable = value
                self.timestamp = write_var_reply.timestamp

                if self.address == self.leader:
                    # make a backup of the new value in the next node
                    self.backup_variable()

                return write_var_reply.timestamp

            except grpc.RpcError as e:
                logging.warning(msg=f"Leader could not be reached: {e.code()}.")

                self.repair_topology(self.leader)

            counter += 1

    def backup_variable(self):
        if self.address == self.next:
            # I am alone
            return

        try:
            self.hub.get_next().WriteVar(sv.WriteVarReq(variable=self.variable))
        except grpc.RpcError as e:
            logging.warning(f"Backup failed: {e.code()}.")

    def leave(self):
        if self.address == self.prev:
            # I am the only node
            return

        try:
            prev_node = self.hub.get_prev()
            prev_node.NodeMissing(sv.NodeMissingMsg(address=self.address))
        except grpc.RpcError as e:
            logging.error(msg="Failed to send leaving message.", exc_info=e)
            raise e

        if self.address == self.leader:
            try:
                # start leader election on the next node
                self.hub.get_next().Election(sv.ElectionMsg(timestamp=-1))
            except grpc.RpcError as e:
                logging.error(msg="Failed to elect a new leader.", exc_info=e)
                print("Trying to rejoin cluster...")
                try:
                    join_reply = self.hub.get_prev().Join(sv.JoinReq(address=self.address))
                    self.hub.reset_stubs()
                    self.next = join_reply.next
                    self.prev = join_reply.prev
                    self.nnext = join_reply.nnext
                    self.leader = join_reply.leader
                except grpc.RpcError as e2:
                    logging.critical(msg="Failed to rejoin. The cluster is now in an undefined state. "
                                         "Restart of the entire cluster is highly recommended.", exc_info=e2)
                    raise e2
                raise e

    def stop(self, status, last_message=""):
        print("Stopping server...")
        self.server.stop(4)
        if last_message == "":
            print(f"{self} stopped.")
        else:
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

    logging.basicConfig(level=logging.INFO,
                        format='%(relativeCreated)6d %(threadName)s %(message)s',
                        filename=f'../logs/{config_node_id}.log',
                        filemode='w')

    config = get_yaml_config(config_node_id)
    Node.this_node = Node(config)
    Node.this_node.run()
