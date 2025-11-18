## Epic GitHub Issue Creator

When this command is invoked:

1. **Check if parameters were provided**:
   - If a file path or issue reference was provided as a parameter, assume this is the reference to the data that will form the basis for this work

2. Use the git-github-operator agent to create a GitHub Epic issue from the plan file or issue passed as the parameter. Also create any constituent sub-tasks as issues. After creating sub-issues, update the Epic with actual links to the sub-issues. 

Study any existing Epic patterns, if present, for example:
- https://github.com/foo/bar/issues/109
- https://github.com/foo/bar/issues/74

Tag the Epic issue with the tag `epic` -- if this is not yet present, create the tag first.
