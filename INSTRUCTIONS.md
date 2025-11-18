# Claude Code Workshop Instructions

For pre-requisites, see [docs/PREREQS.md](docs/PREREQS.md).

> [!WARNING]
> For workshop convenience, there is a settings file with a lot of pre-approved commands, which in general is a **bad idea**. Review carefully: [.claude/settings.local.json.unsafe](.claude/settings.local.json.unsafe). If, after review, you trust the repository, and wish to make use of this, rename it, removing the `.unsafe` suffix. 

Clone this repository, and remove its `.git` folder:

```
git clone git@github.com:xpqz/claudews.git link_check
cd link_check
rm -rf .git
```

Open the cloned repository in VS Code, select a file, and start the Claude Code extension by clicking the little brown "splash" in the tab bar.

After reviewing carefully, execute the following commands to set up the project's initial state:

```
/rules
/make_project link_check
```

## Task

The docs team struggle with ensuring that links are valid. This is a common issue with mkdocs, and it's compounded in our case by two factors:

1. The huge size means that build times are at least 30 minutes, which is unergonomic.
2. The use of the monorepo plugin (site-of-sites) mean that cross-site links are hard to get right, as mkdocs demand relative links, and with the monorepo, relative links don't quite follow the source file system, only the post-build site's hierarchy. Authors inevitably, and understandably, get it wrong.

Our job is to write a spider to help the docs team verify links. The docs team primarily use Docker for their tooling, so we'll fall in with that. They already have a Docker-based preview tool, but it's unsuitable for our needs: it uses `mkdocs serve` which is single-thread Python, rendering on demand -- it would be too slow. Instead, we'll make a docker compose tool that spins up an industry-strength webserver, [nginx](https://nginx.org/), builds the mkdocs site, and serves it up. We'll link-check against that.

Next task is the link-checker itself -- also for Docker. Here, we want to take advantage of docker-compose's clever internal networking. Whilst running against the nginx-container from the "outside" is likely fast enough, running over Docker's internal network will guarantee that we can access pages with near-zero network latency, and be mostly compute-bound. We want to be able to do something like (command names TBD, obviously):

```
docker compose up docs-nginx
# wait for build...

# After completion, in a different terminal:
docker compose run --rm python check_links.py \
                   --base-url http://docs-nginx:8080 \
                   --output /docs/broken_links.yaml
```

and have the second stage run in a few seconds. 

The docs team has standardised on yaml for tooling report output, and we'll respect that.

Things to look out for:

1. The serving container should not build the mkdocs site when the image is built!
2. The serving container should not need to copy the source files into the container, but should rely on a mount
3. Part of the task here is to make the link checker run fast -- it's possible to make it sub-second. However -- make it work sequentially first! 

### Optimising the link checker

We're likely mostly compute-bound when running docker to docker. Here are some hints for making it speedy:

1. Aim to saturate your machine's full set of cores -- prefer the straight use Python's [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) module, rather than [asyncio](https://docs.python.org/3/library/asyncio.html) or some other "clever" approach.
2. Are there any HTTP-level tricks you can use when verifying that a page exists? 
3. Measure what takes time, and think how to make that faster. Your LLM is good at both.