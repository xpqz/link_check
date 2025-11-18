# Prompts

Suggested prompts. Note that we have two largely orthogonal sub-tasks. 

## Lay down the law

```
/rules
```

Enter planning mode

## Plan A

Create a document `docs/PLAN-A.md`. No implementation yet, just a plan. The goal is to write a docker compose setup that at runtime mounts the source for a mkdocs site, builds the mkdocs site and serves it using `nginx` for speed. Carefully construct a detailed plan, considering how we can iterate and especially test each step. 

## Review docs/PLAN-A.md carefully!

Commit.

## Plan B

Create a document `docs/PLAN-B.md`. No implementation yet, just a plan. The goal is to create a tool `link_check/link_check.py`, crucially running in the same docker compose setup, which should spider the site as served in Docker, and verify every non-external link, reporting back on any 404s. The report should be in yaml, and map the page to any broken links. Also verify the nav itself: if any links presented by the nav are broken, report those, too. 

Consider performance implications. Note CAREFULLY: as we're running against a local Docker container, we're compute bound, NOT IO bound: we want multiple processes, not asyncio. Fast, concise, simple to understand and correct. 

Create a separate mkdocs site that we can use for testing the Docker set-up as we're implementing, as building the full site can take up to 30 minutes. Make sure the plan covers this aspect: `test-docs/`. 

## Review docs/PLAN-B.md carefully!

Commit.

## Make a TODO-A.md

Write a detailed document `docs/TODO-A.md`, derived from `docs/PLAN-A.md` which breaks the plan into task-sized chunks of a suitable granularity that can be tested in isolation.

## Review docs/TODO-A.md carefully!

Commit.

## Make a TODO-B.md

Write a detailed document `docs/TODO-B.md`, derived from `docs/PLAN-B.md` which breaks the plan into task-sized chunks of a suitable granularity that can be tested in isolation.

## Review docs/TODO-B.md carefully!

Commit.

## Make Epics and Issues

From `docs/TODO-A.md`, instruct the git-github-operator agent to create two Epic issues: one for the serving, and one for the link checking. They should each clearly state the scope (from the docs/TODO-A.md and/or docs/PLAN-A.md), and list a set of sub-tasks, with check boxes, linking to issues you create for each task. Create issues in implementation order. Label the epics with the 'epic' label, and explicitly reference the PLAN-A.md and TODO-A.md documents, with links. Each issue should reference the #id of the Epic they form part of, and that they're part of phase A.

## (same for phase B)

## Clear!

```
/clear
```
