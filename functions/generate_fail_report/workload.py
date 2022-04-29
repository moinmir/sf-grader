from datetime import datetime, timezone
from functools import reduce
import json
import os

def handle(req, syscall):
    args = req["args"]
    workflow = req["workflow"]
    context = req["context"]
    print("\n\n\n\n===========================================================================================================================================")
    print("GENERATE FAIL REPORT HANDLE")

    
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
    print("\n\n\n\n===========================================================================================================================================")
    print("GENERATE FAIL REPORT")
    print("Args")
    print(args)
    print("context")
    print(context)
    print("Syscall")
    print(syscall)

    print("here 1")
    test_lines = [ json.loads(line) for line in syscall.read_key(bytes(args["test_results_fail"], "utf-8")).split(b'\n') ]
    # test_runs = dict((line['test'], line) for line in test_lines if 'test' in line)
    
    # print(test_lines)
    # for i in range(0, test_lines.find(".go")):
        
    
    print(test_lines[ ])
    print("here 2")

    
    output = []
    formatted_submission_ts = datetime.utcfromtimestamp(context["push_date"]).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%D %T %z')
    
    print("here 3")
    output.append("Submitted %s\n" % formatted_submission_ts)
    output.append("## Compilation error")

    for line in test_lines:
        output.append("### %s" % (line))
        
    
    # key = "%s-report.md" % os.path.splitext(args["grade_report"])[0]
    # syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(output), 'utf-8'))

    print("CONGRATULATIONS YOU KNOW HOW TO RUN CODE.")
    print(output)
    print("======================================\n\n\n\n")
    return { "report": key }
