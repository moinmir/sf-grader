import json

def handle(req, syscall):
    args = req["args"]
    workflow = req["workflow"]
    context = req["context"]
    result = app_handle(args, context, syscall)
    if len(workflow) > 0:
        next_function = workflow.pop(0)
        print("\nNext function: %s" % next_function)
        print("================================================================================\n\n\n\n")
        syscall.invoke(next_function, json.dumps({
            "args": result,
            "workflow": workflow,
            "context": context
        }))
    return result

def app_handle(args, state, syscall):
    print("\n\n\n\n================================================================================")
    print("POST COMMENT")
    print("========================================================================================\n\n\n\n")
    report = syscall.read_key(bytes(args["report"], "utf-8"))
    api_route = "/repos/%s/commits/%s/comments" % (state["repository"], state["commit"])
    body = {
        "body": report.decode()
    }
    resp = syscall.github_rest_post(api_route, body);

    return json.loads(resp.data)
