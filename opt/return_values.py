from collections import namedtuple

def generate_ab():
    a = 'string a'
    b = 'string b'
    return_dict = {
        'val_a': a,
        'val_b': b
    }
    return return_dict

#print(generate_ab()['val_a'])

def named_tuple_ab():
    Keys = namedtuple("Keys", ["public_key", "private_key"])
    keys = Keys('pub','priv')
    return keys

print(named_tuple_ab().private_key)
    