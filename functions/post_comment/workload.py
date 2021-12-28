import json

def handle(req, syscall):
    report = syscall.read_key(bytes(req["report"], "utf-8"))
    api_route = "/repos/%s/commits/%s/comments" % (req["repository"], req["commit"])
    body = {
        "body": report.decode()
    }
    resp = syscall.github_rest_post(api_route, body);

    return json.loads(resp.data)
