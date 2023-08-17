def generate_ab():
    a = 'string a'
    b = 'string b'
    return_dict = {
        'val_a': a,
        'val_b': b
    }
    return return_dict

print(generate_ab()['val_a'])