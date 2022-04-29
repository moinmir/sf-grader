import json
import tempfile
import os
import subprocess

def handle(req, syscall):
    args = req["args"]
    workflow = req["workflow"]
    context = req["context"]
    result = app_handle(args, context, syscall)
    if len(workflow) > 0:
        next_function = workflow.pop(0)
        syscall.invoke(next_function, json.dumps({
            "args": result,
            "workflow": workflow,
            "context": context
        }))
    return result

def app_handle(args, state, syscall):
    os.system("ifconfig lo up")
    # Fetch and untar submission tarball
    assignment = state["metadata"]["assignment"]
    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as submission_tar:
        submission_tar_data = syscall.read_key(bytes(args["submission"], "utf-8"))
        submission_tar.write(submission_tar_data)
        submission_tar.flush()
        with tempfile.TemporaryDirectory() as submission_dir:
            os.system("mkdir %s" % submission_dir)
            os.system("tar -C %s -xzf %s --strip-components=1" % (submission_dir, submission_tar.name))

            # Fetch and untar grading script tarball
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as script_tar:
                script_tar_data = syscall.read_key(bytes("cos316/%s/grading_script" % assignment, "utf-8"))
                script_tar.write(script_tar_data)
                script_tar.flush()
                with tempfile.TemporaryDirectory() as script_dir:
                    os.system("tar -C %s -xzf %s" % (script_dir, script_tar.name))

                    # OK, run tests
                    os.putenv("GOCACHE", "%s/.cache" % script_dir)
                    os.putenv("GOROOT", "/srv/usr/lib/go") 
                    os.putenv("SOLUTION_DIR", submission_dir)
                    os.putenv("PATH", "%s:%s" % ("/srv/usr/lib/go/bin", os.getenv("PATH")))
                    os.chdir(script_dir)
                    if os.path.exists("pretest") and os.access("pretest", os.X_OK):
                        os.system("./pretest")
                    compiledtest = subprocess.Popen("go test -c -o /tmp/grader", shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    compileout, compileerr = compiledtest.communicate()

                    final_results = []
                    
                    if compiledtest.returncode != 0:
                        
                        print({ "error": { "compile": str(compileerr), "returncode": compiledtest.returncode } })
                        # return { "error": { "compile": str(compileerr), "returncode": compiledtest.returncode } }
                    testrun = subprocess.Popen("/tmp/grader -test.v | /srv/usr/lib/go/pkg/tool/linux_amd64/test2json", shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

                    # i = True                     
                    for test_result in testrun.stdout:
                        # if i:
                        #     print("\n\n\n========================")
                        #     print(test_result) 
                        #     i = False
                        # else:
                        #     print(test_result)
                        tr = json.loads(test_result)     

                        # print("\n\n\n========================here")
                        # print(tr)
                        # print("========================\n\n\n")

                        # {'Action': 'output', 'Test': 'TestNegate', 'Output': '=== RUN   TestNegate\n'}

                        if tr["Action"] in ["pass", "fail", "run"]:
                            tr = dict((name.lower(), val) for name, val in tr.items())
                            final_results.append(json.dumps(tr))
                    # print("========================\n\n\n")

                    # print("\n\n\n========================here")
                    # # ['{"action": "run", "test": "TestNegate"}', '{"action": "pass", "test": "TestNegate"}', '{"action": "pass"}']
                    # print(final_results)
                    # print("=======================\n\n\n")
                    key = os.path.join(os.path.splitext(args["submission"])[0], "test_results.jsonl")
                    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(final_results), "utf-8"))
                    testrun.wait()
                    print("\n\n\n========================here")
                    # ['{"action": "run", "test": "TestNegate"}', '{"action": "pass", "test": "TestNegate"}', '{"action": "pass"}']
                    print(key)
                    print("=======================\n\n\n")
                    if testrun.returncode >= 0:
                        return { "test_results": key }
                    else:
                        _, errlog = testrun.communicate()
                        return { "error": { "testrun": str(errlog), "returncode": testrun.returncode } }
    return {}


# b'{"Action":"run","Test":"TestNegate"}\n'
# b'{"Action":"output","Test":"TestNegate","Output":"=== RUN   TestNegate\\n"}\n'
# b'{"Action":"output","Test":"TestNegate","Output":"--- PASS: TestNegate (0.00s)\\n"}\n'
# b'{"Action":"pass","Test":"TestNegate"}\n'
# b'{"Action":"output","Output":"PASS\\n"}\n'
# b'{"Action":"pass"}\n'


# ^[[A{'error': {'compile': "b'# example.com/example\\n../tmpzhvhm_58/example.go:4:9: cannot use !x (type bool) as type string in return argument\\n'", 'returncode': 2}}
