import json
import tempfile
import os

def handle(req, syscall):
    # Fetch and untar grading script tarball
    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as script_tar:
        script_tar_data = syscall.read_key(bytes(req["script"], "utf-8"))
        script_tar.write(script_tar_data)
        script_tar.flush()
        with tempfile.TemporaryDirectory() as script_dir:
            os.system("tar -C %s -xzf %s" % (script_dir, script_tar.name))

            # Fetch and untar submission tarball
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as submission_tar:
                submission_tar_data = syscall.read_key(bytes(req["submission"], "utf-8"))
                submission_tar.write(submission_tar_data)
                submission_tar.flush()
                with tempfile.TemporaryDirectory() as submission_dir:
                    os.system("mkdir %s/src" % submission_dir)
                    os.system("tar -C %s/src/ -xzf %s --strip-components=1" % (submission_dir, submission_tar.name))

                    # OK, run tests
                    os.chdir(script_dir)
                    build_results = os.popen("CGO_ENABLED=0 GOCACHE=%s/.cache GOPATH=%s GOROOT=/srv/usr/lib/go GO111MODULE=off /srv/usr/lib/go/bin/go test -c -o pkg.test 2>&1" % (script_dir, submission_dir)).read()
                    key = os.path.join(os.path.splitext(req["submission"])[0], "test_binary.bin")
                    res = isinstance(open("pkg.test", mode="rb").read(), bytes)
                    syscall.write_key(bytes(key, "utf-8"), open("pkg.test", mode="rb").read())
        return { "test_binary": key, "res": res }
