# Contains utility functions


def address_to_string(address):
    return address.hostname + ":" + str(address.port)


def address1_equals_address2(address1, address2):
    return address1.hostname == address2.hostname and address1.port == address2.port
