import json
import tempfile
import os
import syscalls_pb2

def handle(req, syscall):
    resp = syscall.github_rest_get("/repos/%s/tarball/%s" % (req["repository"]["full_name"], req["after"]));
    key = "github/tarball/%s/%s" % (req["repository"]["full_name"], req["after"]) 
    syscall.write_key(bytes(key, "utf-8"), resp.data)
    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as tmp:
        tmp.write(resp.data)
        with tempfile.TemporaryDirectory() as d:
            os.system("tar -C %s -xzf %s" % (d, tmp.name))
        return { "written": len(resp.data) , "key": key }
