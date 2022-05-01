from datetime import datetime, timezone
import json
import os
import re

def handle(req, syscall):
    args = req["args"]
    workflow = req["workflow"]
    context = req["context"]
    
    result = app_handle(args, context, syscall)
    if len(workflow) > 0:
        next_function = workflow.pop(0)
        print("\nNext function: %s" % next_function)
        print("========================================================================================================================\n\n\n\n")
        syscall.invoke(next_function, json.dumps({
            "args": result,
            "workflow": workflow,
            "context": context
        }))
    return result

def app_handle(args, context, syscall):
    print("\n\n\n\n========================================================================================================================")
    print("Function: GENERATE FAIL REPORT\n")    

    # fetch test results
    test_lines = [ json.loads(line) for line in syscall.read_key(bytes(args["test_results"], "utf-8")).split(b'\n') ]

    err = str(test_lines[0]['error']['compile']).replace("\\n'", "").split("/")
    all_errors = []
    for error in err:
        if re.search(".*:[1-9]*:.*", error):
            error = error.replace("\\n", "")
            all_errors.append(error.replace("..", ""))

    output = []
    formatted_submission_ts = datetime.utcfromtimestamp(context["push_date"]).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%D %T %z')
    output.append("Submitted %s\n" % formatted_submission_ts)
    output.append("## Compilation error")
    for error in all_errors:
        output.append("### %s" % str(error))
 
    # create report 
    grade_report_key = os.path.join(os.path.dirname(args["test_results"]),"grade.json")
    key = "%s-report.md" % os.path.splitext(grade_report_key)[0]
    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(output), 'utf-8'))

    print("Output:\n")
    print(output)

    return { "report": key }
