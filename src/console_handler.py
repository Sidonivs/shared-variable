import threading
import grpc


class ConsoleHandler(threading.Thread):

    def __init__(self, node):
        threading.Thread.__init__(self)
        self.node = node

    def run(self):
        cmd = ""
        while cmd != "q":
            cmd = input("\ncmd > ")
            self.parse_cmd(cmd)

        print("Quiting console handler.")

    def parse_cmd(self, cmd):
        if cmd == "?" or cmd == "help":
            print("? or help - this help")
            print("s - print node status")
            print("r - read shared variable")
            print("w - write to shared variable")
            print("q - nicely ask this node to die and let it say goodbye to it's friends")
            print("k - violently murder this node, other nodes will hate you!")
        elif cmd == "s":
            self.node.print_status()
        elif cmd == "q":
            exit_code = 0
            try:
                self.node.leave()
            except grpc.RpcError as e:
                exit_code = 1
                print(e)
                print("Unsolvable issues encountered, leaving anyway.")
            finally:
                self.node.stop(exit_code, f"{self.node.id.capitalize()} took Death's arm and followed him through the "
                                          f"doors \n"
                                          f"and onto the black desert \n"
                                          f"under the endless night. \n"
                                          f"- T. Pratchett")
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
                print("Unable to retrieve the variable due to an unexpected error or timeout. You may try again later.")

        elif cmd == "w":
            value = input("Value: ")
            try:
                self.node.write_to_shared_variable(value)
                print(f"[{self.node.timestamp}] Write successful.")
            except grpc.RpcError:
                print("Unable to write to the variable due to an unexpected error or timeout. You may try again later.")

        else:
            print("Unrecognized command.")
