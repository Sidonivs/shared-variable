import threading
import grpc


class ConsoleHandler(threading.Thread):

    def __init__(self, node):
        threading.Thread.__init__(self)
        self.node = node

    def run(self):
        print("Welcome to shared variable distributed system. Type '?' to see possible commands.")

        cmd = ""
        while cmd != "q" or cmd != "k":
            cmd = input("\ncmd > ")
            self.parse_cmd(cmd)

        print("Quiting console handler.")

    def parse_cmd(self, cmd):
        if cmd == "?" or cmd == "help":
            print("? or help - this help")
            print("s - print node status")
            print("c - check topology and repair it if needed")
            print("r - read shared variable")
            print("w - write to shared variable")
            print("q - nicely ask this node to die and let it say goodbye to it's friends")
            print("k - violently murder this node, other nodes will hate you!")
        elif cmd == "s":
            self.node.print_status()
        elif cmd == "c":
            print("Checking topology...")
            try:
                self.node.check_topology()
                print("Topology checked and repaired.")
            except grpc.RpcError as e:
                print("Unable to start checking topology due to an unexpected error. You may try again later or "
                      "restart.")

        elif cmd == "q":
            try:
                self.node.leave()
                self.node.stop(0, f"{self.node.id.capitalize()} took Death's arm and followed him through the "
                                  f"doors \n"
                                  f"and onto the black desert \n"
                                  f"under the endless night. \n"
                                  f"- T. Pratchett")
            except grpc.RpcError as e:
                print("Unable to leave safely!")
                self.node.stop(1)
            except TimeoutError as e2:
                print(e2)
                print("Unable to leave safely!")
                self.node.stop(1)

        elif cmd == "k":
            self.node.kill()
        elif cmd == "r":
            try:
                value = self.node.read_shared_variable()
                if value == "":
                    print(f"[{self.node.timestamp}] Shared variable is empty.")
                else:
                    print(f"[{self.node.timestamp}] Shared variable value: '{value}'")
            except grpc.RpcError:
                print("Unable to retrieve the variable due to an unexpected error. You may try again later or restart "
                      "the cluster.")
            except TimeoutError as e:
                print(e)
                print("Unable to retrieve the variable due to a timeout error. You may try again later or restart the "
                      "cluster.")

        elif cmd == "w":
            value = input("Value: ")
            try:
                timestamp = self.node.write_to_shared_variable(value)
                print(f"[{timestamp}] Write successful.")
            except grpc.RpcError:
                print("Unable to write to the variable due to an unexpected error. You may try again later or restart "
                      "the cluster.")
            except TimeoutError as e:
                print(e)
                print("Unable to write to the variable due to a timeout error. You may try again later or restart the "
                      "cluster.")

        else:
            print("Unrecognized command.")
            print("Type '?' or 'help' for help.")
