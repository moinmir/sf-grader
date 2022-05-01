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

    # parse error message    
    err = str(test_lines[0]['error']['compile']).replace("\\n'", "").split("/")[3]
    
    # format output
    output = []
    formatted_submission_ts = datetime.utcfromtimestamp(context["push_date"]).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%D %T %z')
    output.append("Submitted %s\n" % formatted_submission_ts)
    output.append("## Compilation error")
    output.append("### %s" % (err))

    # create report 
    grade_report_key = os.path.join(os.path.dirname(args["test_results"]),"grade.json")
    key = "%s-report.md" % os.path.splitext(grade_report_key)[0]
    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(output), 'utf-8'))

    print("Output:\n")
    print(output)

    return { "report": key }
