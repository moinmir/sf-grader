import json
import tempfile
import os
import subprocess

def handle(req, syscall):
    args = req["args"]
    context = req["context"]
    workflow = req["workflow"]
    result = app_handle(args, context, syscall)
    
    if "error" in result and "compile" in result["error"]:
        workflow =  req["workflowfail"]
    else:
        workflow = req["workflow"]
        
    if len(workflow) > 0:
        next_function = workflow.pop(0)
        print("\n\nNext function: %s" % next_function)
        print("================================================\n\n\n\n")
        syscall.invoke(next_function, json.dumps({
            "args": result,
            "workflow": workflow,
            "context": context
        }))
    return result

def app_handle(args, state, syscall):
    print("\n\n\n\n========================================")
    print("GO GRADER")
    os.system("ifconfig lo up")
    # Fetch and untar submission tarball
    assignment = state["metadata"]["assignment"]
    with tempfile.NamedTemporaryFile(suffix=".tar.gz") as submission_tar:
        submission_tar_data = syscall.read_key(bytes(args["submission"], "utf-8"))
        submission_tar.write(submission_tar_data)
        submission_tar.flush()
        with tempfile.TemporaryDirectory() as submission_dir:
            os.system("mkdir -p %s" % submission_dir)
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
                        print("COMPILATION FAILED\n\n")
                        out = { "error": { "compile": str(compileerr), "returncode": compiledtest.returncode } }
                        final_results.append(json.dumps(out))
                        print(final_results)
                        key = os.path.join(os.path.splitext(args["submission"])[0], "test_results.jsonl")
                        syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(final_results), "utf-8"))

                        return out
                    print("COMPILATION SUCCEEDED\n\n")
                    
                    testrun = subprocess.Popen("/tmp/grader -test.v | /srv/usr/lib/go/pkg/tool/linux_amd64/test2json", shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

                    for test_result in testrun.stdout:
                        tr = json.loads(test_result)
                        print(tr)   

                        if tr["Action"] in ["pass", "fail", "run"]:
                            tr = dict((name.lower(), val) for name, val in tr.items())
                            final_results.append(json.dumps(tr))
                    print(final_results)
                    key = os.path.join(os.path.splitext(args["submission"])[0], "test_results.jsonl")
                    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(final_results), "utf-8"))
                    testrun.wait()
                    if testrun.returncode >= 0:
                        return { "test_results": key }
                    else:
                        _, errlog = testrun.communicate()
                        print("Error log:")
                        print(errlog)
                        return { "error": { "testrun": str(errlog), "returncode": testrun.returncode } }
    return {}


# {'Action': 'run', 'Test': 'TestNegate'}
# {'Action': 'output', 'Test': 'TestNegate', 'Output': '=== RUN   TestNegate\n'}
# {'Action': 'output', 'Test': 'TestNegate', 'Output': '--- FAIL: TestNegate (0.00s)\n'}
