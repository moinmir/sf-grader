import os
import json


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


def app_handle(args, context, syscall):
    print("\n\n\n\n========================================\n")
    print("Function: GRADES")
    print(args["test_results"])

    test_lines = [json.loads(line) for line in syscall.read_key(
        bytes(args["test_results"], "utf-8")).split(b'\n')]
    test_runs = dict((line['test'], line)
                     for line in test_lines if 'test' in line)
    print("test_runs: %s" % test_runs)
    grader_config = "cos316/%s/grader_config" % context["metadata"]["assignment"]

    config = json.loads(syscall.read_key(bytes(grader_config, "utf-8")))
    
    total_points = sum([test["points"] for test in config["tests"].values(
    ) if "extraCredit" not in test or not test["extraCredit"]])

    tests = []
    for (test_name, conf) in config["tests"].items():
        if test_name in test_runs:
            test = test_runs[test_name].copy()
            test["conf"] = conf
            test["subtests"] = {key: val for key, val in test_runs.items(
            ) if key.startswith("%s/" % test_name)}
            tests.append(test)

    points = 0.0
    for test in tests:
        if test["action"] == "pass":
            points += test["conf"]["points"]

    output = {
        "points": points,
        "possible": total_points,
        "grade": points / total_points,
        "tests": tests,
        "push_date": context["push_date"]
    }

    key = os.path.join(os.path.dirname(args["test_results"]), "grade.json")
    syscall.write_key(bytes(key, "utf-8"), bytes(json.dumps(output), "utf-8"))

    print("\nFINISHED RUNNING")
    print("================================================\n\n\n\n")

    return {
        "grade": points / total_points,
        "grade_report": key
    }
