def dict_to_utf8(byte_dict):
    """ decode keys and values to utf-8 recursively """
    decoded_dict = {}
    for key, val in byte_dict.items():
        key = key.decode('utf-8')
        if type(val) is dict:
            val = dict_to_utf8(val)
        # else:
        try:
            # 'pieces' needs to be kept as bytes
            if key != 'pieces':
                val = val.decode('utf-8')
        except:
            pass
        decoded_dict[key] = val
    return decoded_dict
