def list_to_hex_str(data, delimiter=""):
    data_string = delimiter.join(["{0:02x}".format(i) for i in data])
    return data_string
