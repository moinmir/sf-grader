import json

def handle(req, syscall):
    test_lines = [ json.loads(line) for line in syscall.read_key(bytes(req["test_results"], "utf-8")).split(b'\n') ]
    test_runs = dict((line['test'], line) for line in test_lines if 'test' in line)

    config = json.loads(syscall.read_key(bytes(req["grader_config"], "utf-8")))

    total_points = sum([ test["points"] for test in config["tests"].values() if "extraCredit" not in test or not test["extraCredit"]])

    tests = []
    for (test_name, conf) in config["tests"].items():
        if test_name in test_runs:
            test = test_runs[test_name].copy()
            test["conf"] = conf
            test["subtests"] = { key:val for key, val in test_runs.items() if key.startswith("%s/" % test_name) }
            tests.append(test)

    points = 0.0
    for test in tests:
        if test["action"] == "pass":
            points += test["conf"]["points"]

    output = {
        "points": points,
        "possible": total_points,
        "grade": points / total_points,
        "tests": tests
        }

    key = "%s/grade" % req["submission"]
    syscall.write_key(bytes(key, "utf-8"), bytes(json.dumps(output), "utf-8"))

    return {
        "grade": points / total_points,
        "output": key
        }
