import json
import tempfile
import os
import syscalls_pb2

def handle(req, syscall):
    # Fetch and untar grading script tarball
    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as script_tar:
        script_tar_data = syscall.read_key(bytes(req["script"], "utf-8"))
        script_tar.write(script_tar_data)
        with tempfile.TemporaryDirectory() as script_dir:
            os.system("tar -C %s -xzf %s" % (script_dir, script_tar.name))

            # Fetch and untar submission tarball
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as submission_tar:
                submission_tar_data = syscall.read_key(bytes(req["submission"], "utf-8"))
                submission_tar.write(submission_tar_data)
                with tempfile.TemporaryDirectory() as submission_dir:
                    os.system("mkdir %s/src" % submission_dir)
                    os.system("tar -C %s/src/ -xzf %s --strip-components=1" % (submission_dir, submission_tar.name))

                    # OK, run tests
                    os.chdir(script_dir)
                    test_results = os.popen("GOCACHE=%s/.cache GOPATH=%s GOROOT=/srv/usr/lib/go GO111MODULE=off /srv/usr/lib/go/bin/go test -json" % (script_dir, submission_dir)).read()
                    final_results = []
                    for test_result in test_results.splitlines():
                        tr = json.loads(test_result)
                        if tr["Action"] != "output":
                            final_results.append(test_result)
                    key = "%s/test_results" % req["submission"]
                    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(final_results), "utf-8"))
        return { "test_results": key }
