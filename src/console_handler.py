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
        if cmd == "?":
            print("? - this help")
            print("s - print node status")
            print("r - read shared variable")
            print("w - write to shared variable")
        elif cmd == "s":
            self.node.print_status()
        elif cmd == "q":
            self.node.leave()
            self.node.stop(0)
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
