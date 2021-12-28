import json
import tempfile
import os

def handle(req, syscall):
    # Fetch and untar grading script tarball
    with tempfile.NamedTemporaryFile(delete=False) as test_binary:
        test_binary_data = syscall.read_key(bytes(req["test_binary"], "utf-8"))
        test_binary.write(test_binary_data)
        test_binary.flush()
        os.system("chmod +x %s" % test_binary.name)
        test_binary.close()
        test_results = os.popen("%s | /srv/usr/lib/go/pkg/tool/linux_amd64/test2json 2>&1" % (test_binary.name)).read()
        os.remove(test_binary.name)
        final_results = []
        for test_result in test_results.splitlines():
            tr = json.loads(test_result)
            if tr["Action"] in ["pass", "fail"]:
                tr = dict((name.lower(), val) for name, val in tr.items())
                final_results.append(json.dumps(tr))
        key = os.path.join(os.path.dirname(req["test_binary"]), "test_results.jsonl")
        syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(final_results), "utf-8"))
        return { "test_results": key }
