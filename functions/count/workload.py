import json
import struct
import syscalls_pb2

def handle(obj, syscall):
    l = syscalls_pb2.DcLabel(secrecy = syscalls_pb2.Component(clauses = [ syscalls_pb2.Clause(principals = ["Amit"])]))
    cl = syscall.taint(l)
    old = syscall.read_key(bytes("count", "utf-8"))
    count = 0
    if old:
        count = struct.unpack(">I", old)[0]
    syscall.write_key(bytes("count", "utf-8"), struct.pack(">I", count + 1))
    return {'count': count }
