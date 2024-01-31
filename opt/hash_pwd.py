from opt.hasher import Hasher as sta_hasher
dpwd = sta_hasher(['a']).generate()

print(dpwd[0])