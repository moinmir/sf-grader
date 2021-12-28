from functools import reduce
import json
import os

def handle(req, syscall):
    grade = json.loads(syscall.read_key(bytes(req["grade"], "utf-8")))

    correctness_tests = [ test for test in grade["tests"] if not ("performance" in test["conf"] and test["conf"]["performance"]) ]
    performance_tests = [ test for test in grade["tests"] if ("performance" in test["conf"] and test["conf"]["performance"]) ]

    tests_passed = len([ test for test in grade["tests"] if test["action"] == "pass"])
    all_subtests = reduce(lambda a,b: list(a) + list(b), map(lambda t: t['subtests'].items(), grade["tests"]))
    passed_subtests = len([ test for test in all_subtests if test[1]["action"] == "pass"])

    output = []

    output.append("## Grade: %.2f%%" % (grade["grade"] * 100))
    output.append("  * %d points of a possible %d" % (grade["points"], grade["possible"]))
    output.append("  * Passed   %d / %d  tests     (%d failed)" % (tests_passed, len(grade["tests"]), len(grade["tests"]) - tests_passed))
    output.append("    * Passed  %d / %d subtests  (%d failed)" % (passed_subtests, len(all_subtests), len(all_subtests) - passed_subtests))

    output.append("## Correctness Tests")
    for i, test in enumerate(correctness_tests):
        output.append("### %d. %s" % (i + 1, test["conf"]["desc"]) )
        for subtest, res in test["subtests"].items():
            parts = "/".join(subtest.split("/")[1:])
            parts = parts.split("&")
            output.append("  > {0: >10} {1: <50} ...{2}".format(parts[0], parts[1], "FAIL" if res["action"] == "fail" else "ok"))
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
    key = "%s-report.md" % os.path.splitext(req["grade"])[0]
    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(output), 'utf-8'))
    return { "report": key }
