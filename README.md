# SnapFaas Grading Functions for COS316

## Directory structure

For each "function" `FUNC_NAME` there are three important important artifacts:

1. `functions/FUNC_NAME/` is a subdirectory containing the function code, mounted as `/srv/` when
   the function is running.
2. `payloads/FUNC_NAME.jsonl` is a JSON-line formatted file where each line is
   a JSON encoded request payload to the function, useful for testing.
3. `output/FUNC_NAME.img` a "compiled" filesystem image from the function
   source automatically generated.

The `storage` sub-directory is used to store LMDB data from test runs.

## Test functions

To run a function using the requests in its respective payload file, use the
Makefile in the root directory:

```
$ make run/FUNC_NAME
```

This will build the function image and run it using `fc_wrapper`, passing in
each of the requests from the payload one after the other. It stores the output
of in `run/FUNC_NAME`.

## Objects

- `github/[owner]/[repo]/_meta` - JSON object with assignment and list of student NetIDs
  Ex: `github/cos316/assignment0-foobar/_meta`
  ```json
  { "assignment": "assignment0", "users": [ "aalevy", "kap" ] }
  ```

- `github/[owner]/[repo]/_workflow` - JSON array with workflow functions
  Ex: `github/cos316/assignment0-foobar/_workflow`
  ```json
  [ "go_grader", "grades", "generate_report", "post_comment" ]
  ```
 
- `cos316/[assignment]/grading_script` - tarball of the grading script

- `cos316/[assignment]/grader_config` - JSON configuration from grading script
