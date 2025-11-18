# TODO-A: Docker Compose MkDocs + Nginx Setup

Derived from [PLAN-A.md](PLAN-A.md)

## Phase 1: Test MkDocs Site Creation ✓ COMPLETED

### Task 1.1: Create Test Site Directory Structure ✓
- [x] Create `tmp/test-mkdocs/` directory
- [x] Create `tmp/test-mkdocs/docs/` subdirectory

**Testing:** Verify directories exist with `ls -la tmp/test-mkdocs/`

### Task 1.2: Create Minimal mkdocs.yml Configuration ✓
- [x] Create `tmp/test-mkdocs/mkdocs.yml`
- [x] Configure Material theme
- [x] Add navigation.instant and navigation.tracking features
- [x] Add search plugin (privacy plugin not available in PyPI)
- [x] Add markdown extensions: admonition, pymdownx.superfences, pymdownx.details, toc
- [x] Define navigation structure (Home, Page 1, Page 2)

**Testing:** Validate YAML syntax with `python -c "import yaml; yaml.safe_load(open('tmp/test-mkdocs/mkdocs.yml'))"`

### Task 1.3: Create Sample Content with Link Variations ✓
- [x] Create `tmp/test-mkdocs/docs/index.md` with internal link, anchor link, external link
- [x] Create `tmp/test-mkdocs/docs/page1.md` with links to home, page2, and anchor on page2
- [x] Create `tmp/test-mkdocs/docs/page2.md` with section heading

**Testing:** Verify markdown files created with `cat tmp/test-mkdocs/docs/*.md`

### Task 1.4: Validate Local MkDocs Build ✓
- [x] Run `mkdocs build` from `tmp/test-mkdocs/`
- [x] Verify exit code is 0
- [x] Verify `site/` directory created with HTML files
- [x] Inspect generated HTML for proper link structure

**Testing:**
```bash
cd tmp/test-mkdocs && mkdocs build
echo $?  # Should be 0
ls -la site/
grep -r "href" site/*.html
```

### Task 1.5: Validate Local MkDocs Serve ✓
- [x] Run `mkdocs serve` from `tmp/test-mkdocs/`
- [x] Verify serves on http://localhost:8000
- [x] Manually test internal links work
- [x] Manually test anchor links work
- [x] Verify external link exists (not followed)

**Testing:** Access http://localhost:8000 and click through all links

**Completed:** Issue #1, PR #8

---

## Phase 2: Basic Nginx Container (Testable Standalone)

### Task 2.1: Create Nginx Dockerfile
- [ ] Create `docker/nginx/` directory
- [ ] Create `docker/nginx/Dockerfile` based on nginx:alpine
- [ ] Set EXPOSE 8080

**Testing:** Build with `docker build -t test-nginx docker/nginx/`

### Task 2.2: Create Nginx Configuration
- [ ] Create `docker/nginx/nginx.conf`
- [ ] Configure server block listening on port 8080
- [ ] Set root to `/usr/share/nginx/html`
- [ ] Set index to `index.html`
- [ ] Add location block with `try_files`

**Testing:** Validate nginx config syntax in container: `docker run --rm -v $(pwd)/docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro nginx:alpine nginx -t`

### Task 2.3: Build Test Site to Bind Mount Directory
- [ ] Create `tmp/test-site-output/` directory
- [ ] Run `mkdocs build --site-dir ../test-site-output` from `tmp/test-mkdocs/`
- [ ] Verify HTML files in `tmp/test-site-output/`

**Testing:** `ls -la tmp/test-site-output/`

### Task 2.4: Create Initial docker-compose.yml with Nginx Service
- [ ] Create `docker-compose.yml` in project root
- [ ] Define `docs-nginx` service
- [ ] Configure build context pointing to `docker/nginx`
- [ ] Set container name to `docs-nginx`
- [ ] Map port `8080:8080`
- [ ] Mount `./tmp/test-site-output:/usr/share/nginx/html:ro`

**Testing:** Validate compose syntax with `docker compose config`

### Task 2.5: Test Nginx Container from Host
- [ ] Run `docker compose up docs-nginx`
- [ ] Verify container starts without errors
- [ ] Test with `curl http://localhost:8080`
- [ ] Verify HTML content returned
- [ ] Test accessing specific pages: `curl http://localhost:8080/page1/`

**Testing:** Check HTTP status codes are 200

### Task 2.6: Test Nginx Container from Another Container
- [ ] Start docs-nginx with `docker compose up -d docs-nginx`
- [ ] Run curl from another container: `docker run --rm --network link_check_default curlimages/curl curl http://docs-nginx:8080`
- [ ] Verify content returned

**Testing:** Verify container name resolution works on docker network

### Task 2.7: Measure Nginx Response Time Baseline
- [ ] Run `time curl http://localhost:8080 > /dev/null` multiple times
- [ ] Document average response time
- [ ] Verify sub-millisecond response over internal network

**Testing:** Record baseline performance metrics

---

## Phase 3: MkDocs Builder Container (Testable Standalone)

### Task 3.1: Create MkDocs Requirements File
- [ ] Create `docker/mkdocs/` directory
- [ ] Create `docker/mkdocs/requirements.txt`
- [ ] Add mkdocs>=1.5.0
- [ ] Add mkdocs-material>=9.5.0
- [ ] Add mkdocs-privacy-plugin
- [ ] Add pymdown-extensions

**Testing:** Validate package names exist on PyPI

### Task 3.2: Create MkDocs Builder Dockerfile
- [ ] Create `docker/mkdocs/Dockerfile` based on python:3.11-slim
- [ ] Set WORKDIR to `/build`
- [ ] COPY requirements.txt
- [ ] RUN pip install with --no-cache-dir
- [ ] Set CMD to `["mkdocs", "build", "--clean", "--site-dir", "/site"]`

**Testing:** Build with `docker build -t test-mkdocs docker/mkdocs/`

### Task 3.3: Add MkDocs Builder Service to docker-compose.yml
- [ ] Add `mkdocs-builder` service definition
- [ ] Configure build context pointing to `docker/mkdocs`
- [ ] Mount `./tmp/test-mkdocs:/docs:ro`
- [ ] Set `working_dir: /docs`
- [ ] Do not define volumes for /site yet (will use named volume later)

**Testing:** Validate compose syntax with `docker compose config`

### Task 3.4: Test Builder with Temporary Output Mount
- [ ] Temporarily add volume mount for testing: `- ./tmp/builder-test-output:/site`
- [ ] Run `docker compose run --rm mkdocs-builder`
- [ ] Verify exit code is 0
- [ ] Verify HTML files created in `tmp/builder-test-output/`

**Testing:**
```bash
docker compose run --rm mkdocs-builder
echo $?  # Should be 0
ls -la tmp/builder-test-output/
```

### Task 3.5: Test Builder Exit Code Propagation
- [ ] Run builder with valid config, verify exit code 0
- [ ] Introduce syntax error in `tmp/test-mkdocs/mkdocs.yml`
- [ ] Run builder, verify exit code non-zero
- [ ] Fix mkdocs.yml
- [ ] Re-run builder, verify exit code 0 again

**Testing:**
```bash
docker compose run --rm mkdocs-builder
echo $?
```

### Task 3.6: Measure Builder Performance
- [ ] Time the build process: `time docker compose run --rm mkdocs-builder`
- [ ] Document build time for test site
- [ ] Establish baseline for cache investigation

**Testing:** Record build time metrics

---

## Phase 4: Integration via Named Volume

### Task 4.1: Define Named Volume in docker-compose.yml
- [ ] Add `volumes:` section at root level
- [ ] Define `site-output:` named volume

**Testing:** Validate compose syntax with `docker compose config`

### Task 4.2: Update Builder to Use Named Volume
- [ ] Remove temporary bind mount from Task 3.4
- [ ] Add volume mount: `- site-output:/site`
- [ ] Keep source mount: `- ./tmp/test-mkdocs:/docs:ro`

**Testing:** Validate compose syntax

### Task 4.3: Update Nginx to Use Named Volume
- [ ] Remove bind mount to `tmp/test-site-output`
- [ ] Add volume mount: `- site-output:/usr/share/nginx/html:ro`

**Testing:** Validate compose syntax

### Task 4.4: Test Build to Named Volume
- [ ] Run `docker compose down -v` to clean volumes
- [ ] Run `docker compose run --rm mkdocs-builder`
- [ ] Verify volume created: `docker volume ls | grep site-output`

**Testing:** Verify volume exists

### Task 4.5: Inspect Named Volume Contents
- [ ] Run temporary container to inspect volume: `docker run --rm -v link_check_site-output:/site alpine ls -la /site/`
- [ ] Verify HTML files present
- [ ] Verify directory structure correct

**Testing:** Check index.html and other pages exist

### Task 4.6: Test Nginx Serving from Named Volume
- [ ] Start nginx: `docker compose up -d docs-nginx`
- [ ] Test with `curl http://localhost:8080`
- [ ] Verify correct content served
- [ ] Check multiple pages

**Testing:** All curl requests return expected HTML

### Task 4.7: Test Rebuild Workflow
- [ ] Modify `tmp/test-mkdocs/docs/index.md` (add marker text)
- [ ] Run `docker compose run --rm mkdocs-builder`
- [ ] Restart nginx: `docker compose restart docs-nginx`
- [ ] Verify updated content served: `curl http://localhost:8080 | grep "marker"`

**Testing:** Updated content should be visible

### Task 4.8: Test Volume Cleanup and Rebuild
- [ ] Run `docker compose down -v`
- [ ] Run `docker compose run --rm mkdocs-builder`
- [ ] Run `docker compose up -d docs-nginx`
- [ ] Verify site serves correctly

**Testing:** Clean rebuild should work without errors

---

## Phase 5: Service-based Orchestration

### Task 5.1: Add Service Dependencies to docker-compose.yml
- [ ] Add `depends_on:` to `docs-nginx` service
- [ ] Add dependency on `mkdocs-builder` with `condition: service_completed_successfully`

**Testing:** Validate compose syntax

### Task 5.2: Add Nginx Health Check
- [ ] Add `healthcheck:` section to `docs-nginx` service
- [ ] Set test command: `["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080/"]`
- [ ] Set interval: 5s
- [ ] Set timeout: 3s
- [ ] Set retries: 3

**Testing:** Validate compose syntax

### Task 5.3: Test Cold Start Workflow
- [ ] Run `docker compose down -v`
- [ ] Run `docker compose up docs-nginx`
- [ ] Verify builder runs first
- [ ] Verify builder exits with code 0
- [ ] Verify nginx starts after builder completes
- [ ] Verify nginx becomes healthy

**Testing:** Watch compose output, check service order

### Task 5.4: Test Builder Failure Propagation
- [ ] Introduce error in `tmp/test-mkdocs/mkdocs.yml`
- [ ] Run `docker compose down -v`
- [ ] Run `docker compose up docs-nginx`
- [ ] Verify builder fails
- [ ] Verify nginx does NOT start
- [ ] Verify clear error message displayed

**Testing:** Nginx should not start when builder fails

### Task 5.5: Test Warm Restart Workflow
- [ ] Fix `tmp/test-mkdocs/mkdocs.yml`
- [ ] Run `docker compose down` (without -v)
- [ ] Run `docker compose up docs-nginx`
- [ ] Verify rebuild occurs
- [ ] Verify nginx serves updated content

**Testing:** Warm restart should work with existing volumes

### Task 5.6: Measure End-to-End Workflow Time
- [ ] Run `docker compose down -v`
- [ ] Run `time docker compose up docs-nginx`
- [ ] Document total time from start to nginx healthy
- [ ] Document builder time separately
- [ ] Document nginx startup time separately

**Testing:** Record performance metrics

### Task 5.7: Test with Full dyalog-docs Site
- [ ] Update `docker/mkdocs/requirements.txt` with additional plugins:
  - mkdocs-macros-plugin
  - mkdocs-monorepo-plugin
  - mkdocs-minify-plugin
  - mkdocs-caption
  - markdown-tables-extended
- [ ] Update docker-compose.yml to mount dyalog-docs instead of test-mkdocs
- [ ] Run `docker compose down -v`
- [ ] Run `docker compose up docs-nginx`
- [ ] Verify full site builds successfully
- [ ] Verify nginx serves full site
- [ ] Measure build time

**Testing:** Full dyalog-docs site should build and serve correctly

### Task 5.8: Document Workflow and Usage
- [ ] Create usage documentation in docker/README.md or main README
- [ ] Document `docker compose up docs-nginx` command
- [ ] Document rebuild workflow
- [ ] Document cleanup workflow with `docker compose down -v`
- [ ] Document common errors and solutions

**Testing:** Follow documentation from scratch to verify accuracy

---

## Phase 6: Build Cache Investigation

### Task 6.1: Research MkDocs Caching Mechanisms
- [ ] Review MkDocs documentation for caching options
- [ ] Review Material theme documentation for caching
- [ ] Review plugin documentation for cache directories
- [ ] Identify potential cache directories to persist

**Testing:** Document findings

### Task 6.2: Measure Baseline Build Time
- [ ] Use metrics from Task 5.6 and 5.7
- [ ] Document cold build time (no cache)
- [ ] Document warm build time (with cache if any)
- [ ] Identify build bottlenecks

**Testing:** Clear performance data recorded

### Task 6.3: Test Cache Volume Implementation (If Applicable)
- [ ] If caching mechanism identified, add cache volume to docker-compose.yml
- [ ] Update builder to use cache directory
- [ ] Test cold build (no cache)
- [ ] Test warm build (with cache)
- [ ] Measure time difference

**Testing:** Compare build times with and without cache

### Task 6.4: Evaluate Cache Performance Improvement
- [ ] Calculate percentage improvement
- [ ] Evaluate if improvement > 20% threshold
- [ ] Document recommendation: implement or skip caching

**Testing:** Make data-driven decision on caching

### Task 6.5: Implement or Document Cache Decision
- [ ] If >20% improvement: keep cache volume implementation
- [ ] If <20% improvement: remove cache volume, document decision
- [ ] Update documentation with findings

**Testing:** Final compose configuration reflects decision

---

## Phase 7: Link Checker Integration (Future Preparation)

### Task 7.1: Design Link Checker Service (Design Only)
- [ ] Document service definition structure
- [ ] Document volume mounts needed for reports
- [ ] Document network access requirements
- [ ] Document base URL configuration approach

**Testing:** Design document created, no implementation

### Task 7.2: Document Link Checker Usage Pattern (Design Only)
- [ ] Document how to run link checker after docs-nginx is ready
- [ ] Document expected command: `docker compose run --rm link-checker`
- [ ] Document report output location
- [ ] Document network connectivity approach

**Testing:** Usage documentation created

---

## Verification Checklist (End-to-End)

After completing all phases, verify:

- [ ] Single command `docker compose up docs-nginx` builds and serves site
- [ ] Builder exit code propagates correctly (failure prevents nginx start)
- [ ] Nginx serves on port 8080 from host
- [ ] Nginx accessible as `docs-nginx:8080` from other containers
- [ ] Can rebuild with `docker compose down && docker compose up docs-nginx`
- [ ] Can clean rebuild with `docker compose down -v && docker compose up docs-nginx`
- [ ] Test site builds successfully
- [ ] Full dyalog-docs builds successfully
- [ ] No file permission issues with volumes
- [ ] Health checks work correctly
- [ ] Error messages are clear for common failures
- [ ] Documentation is accurate and complete
- [ ] Performance targets met:
  - Test site build < 10 seconds
  - Full dyalog-docs build < 5 minutes (baseline)
  - Nginx response < 10ms over internal network
  - Container startup < 5 seconds

## Notes

- Each task is independently testable
- Tasks within a phase may have dependencies on prior tasks in same phase
- Tasks across phases depend on prior phases being complete
- Stop and request review if any task fails its testing criteria
- Commit working code after each completed phase
- Create git branch before starting Phase 1 implementation
