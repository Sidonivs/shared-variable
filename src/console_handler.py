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
            self.node.leave()
            self.node.stop(0, f"{self.node.id.capitalize()} took Death's arm and followed him through the doors \n"
                              f"and onto the black desert \n"
                              f"under the endless night. \n"
                              f"- T. Pratchett")
        elif cmd == "k":
            self.node.kill()
        elif cmd == "r":
            try:
                value = self.node.read_shared_variable()
                if value == "":
                    print("Shared variable is empty.")
                else:
                    print(f"Shared variable value: '{value}'")
            except grpc.RpcError:
                print("Unable to retrieve the variable due to an unexpected error. You may try again later.")

        elif cmd == "w":
            value = input("Value: ")
            try:
                self.node.write_to_shared_variable(value)
            except grpc.RpcError:
                print("Unable to write to the variable due to an unexpected error. You may try again later.")

        else:
            print("Unrecognized command.")
