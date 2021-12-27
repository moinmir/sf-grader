import json
import tempfile
import os
import syscalls_pb2

def handle(req, syscall):
    resp = syscall.github_rest_get("/repos/%s/tarball/%s" % (req["repository"]["full_name"], req["after"]));
    key = "github/%s/%s.tgz" % (req["repository"]["full_name"], req["after"])
    syscall.write_key(bytes(key, "utf-8"), resp.data)
    return { "written": len(resp.data) , "key": key }
