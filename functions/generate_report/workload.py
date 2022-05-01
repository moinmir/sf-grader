from datetime import datetime, timezone
from functools import reduce
import json
import os

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

# test_runs: {'TestCorrect': {'action': 'pass', 'test': 'TestCorrect'}, 'TestNegate': {'action': 'run', 'test': 'TestNegate'}}
# ## Grade: 0.00%
#   * 0 points of a possible 20
#   * Passed   0 / 0  tests     (0 failed)
#     * Passed  0 / 0 subtests  (0 failed)
# ## Correctness Tests

def app_handle(args, context, syscall):
    print("\n\n\n\n========================================")
    print("Function: GENERATE REPORT\n")

    grader_config = "cos316/%s/grader_config" % context["metadata"]["assignment"]
    config = json.loads(syscall.read_key(bytes(grader_config, "utf-8")))
    delim = config["subtest"]["delim"]
    grade = json.loads(syscall.read_key(bytes(args["grade_report"], "utf-8")))


#  'tests': [{'action': 'run', 'test': 'TestNegate', 'conf': {'desc': 'Negate', 'points': 10.0}, 'subtests': {}}, 
#            {'action': 'pass', 'test': 'TestCorrect', 'conf': {'desc': 'Marina is cool.', 'points': 10.0}, 'subtests': {}}]

    print(grade["tests"])
    broken_tests = []
    for i in range(grade["tests"]):
        if grade["tests"][i]["action"] == "run":
            if (i + 1 < len(grade["tests"]) and grade["tests"][i + 1]["action"] == "run"):
                broken_tests.append(grade["tests"][i])
            if len(grade["tests"]) == i+1:
                broken_tests.append(grade["tests"][i])
    
    grade["tests"] = [test for test in grade["tests"] if test["action"] in ["pass", "fail"]]
    correctness_tests = [ test for test in grade["tests"] if not ("performance" in test["conf"] and test["conf"]["performance"])]
    performance_tests = [ test for test in grade["tests"] if ("performance" in test["conf"] and test["conf"]["performance"]) ]

    tests_passed = len([ test for test in grade["tests"] if test["action"] == "pass"])
    all_subtests = reduce(lambda a,b: list(a) + list(b), map(lambda t: t['subtests'].items(), grade["tests"]), [])
    passed_subtests = len([ test for test in all_subtests if test[1]["action"] == "pass"])
    output = []
    formatted_submission_ts = datetime.utcfromtimestamp(context["push_date"]).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%D %T %z')
    output.append("Submitted %s\n" % formatted_submission_ts)
    output.append("## Grade: %.2f%%" % (grade["grade"] * 100))
    output.append("  * %d points of a possible %d" % (grade["points"], grade["possible"]))
    output.append("  * Passed   %d / %d  tests     (%d failed)" % (tests_passed, len(grade["tests"]), len(grade["tests"]) - tests_passed))
    output.append("    * Passed  %d / %d subtests  (%d failed)" % (passed_subtests, len(all_subtests), len(all_subtests) - passed_subtests))

    output.append("## Correctness Tests")
    for i, test in enumerate(correctness_tests):
        output.append("### %d. %s" % (i + 1, test["conf"]["desc"]) )
        subtests = [(subtest, res) for (subtest, res) in
                test["subtests"].items() if res["action"] in ["pass", "fail"]]
        for subtest, res in subtests:
            parts = "/".join(subtest.split("/")[1:])
            parts = parts.split(delim)
            output.append(">     {0: >10} {1: <50} ...{2}".format(parts[0], parts[1], "FAIL" if res["action"] == "fail" else "ok"))
        if test["action"] == "fail":
            output.append("                               -- test failed (-%d) --" % test["conf"]["points"])
        else:
            output.append("                               -- test passed --")

    if len(performance_tests) > 0:
        output.append("## Performance Tests")
        for i, test in enumerate(performance_tests):
            output.append("### %d. %s" % (i + 1, test["conf"]["desc"]) )
            if test["action"] == "fail":
                output.append("                               -- test failed (-%d) --" % test["conf"]["points"])
            else:
                output.append("                               -- test passed --")
                
    
    if len(broken_tests) > 0:
        output.append("## Broken Tests")
        for i in range(0, len(broken_tests)):
            output.append("### %d. %s" % (i + 1, broken_tests[i]["conf"]["desc"]) )
            output.append("                               -- test TLE'd or Panicked (-%d) --" % broken_tests[i]["conf"]["points"])

    key = "%s-report.md" % os.path.splitext(args["grade_report"])[0]
    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(output), 'utf-8'))
    
    print("\nOutput:")
    print(output)

    return { "report": key }
