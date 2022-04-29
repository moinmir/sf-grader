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

def app_handle(args, context, syscall):
    print("\n\n\n\n==================================================================================")
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
        
    
    err = str(test_lines[0]['error']['compile']).replace("\\n'", "").split("/")[3]
    
    output = []
    formatted_submission_ts = datetime.utcfromtimestamp(context["push_date"]).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%D %T %z')
    
    print("here 3")
    output.append("Submitted %s\n" % formatted_submission_ts)
    output.append("## Compilation error")
    output.append("### %s" % (err))
        
    
    grade_report_key = os.path.join(os.path.dirname(args["test_results"]),"grade.json")
    key = "%s-report.md" % os.path.splitext(grade_report_key)[0]
    syscall.write_key(bytes(key, "utf-8"), bytes('\n'.join(output), 'utf-8'))

    print("CONGRATULATIONS YOU KNOW HOW TO RUN CODE.")
    print(output)
    print(key)
    print("======================================\n\n\n\n")
    return { "report": key }
