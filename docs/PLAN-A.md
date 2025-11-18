# Plan A: Docker Compose MkDocs + Nginx Setup

## Objective

Create a Docker Compose setup that mounts MkDocs source at runtime, builds the site, and serves it using nginx for high-performance link checking.

## Key Constraints

1. Do NOT build the MkDocs site during image build
2. Do NOT copy source files into the container
3. Use volume mounts for source files
4. Serve using nginx for production-like performance
5. Enable fast link checking over Docker internal network
6. Use service-based architecture: `docker compose up docs-nginx` builds and serves
7. Builder must propagate exit codes for failure detection
8. Use port 8080 consistently (no port 80)

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│ Host System                                     │
│  └── tmp/test-mkdocs/ (mounted read-only)      │
└─────────────────────────────────────────────────┘
                    │
                    │ bind mount
                    ↓
┌─────────────────────────────────────────────────┐
│ Builder Container (service, runs once)          │
│  - Python + MkDocs                              │
│  - Reads from /docs (mount)                     │
│  - Builds to /site (named volume)               │
│  - Exits with build status code                 │
└─────────────────────────────────────────────────┘
                    │
                    │ named volume
                    ↓
┌─────────────────────────────────────────────────┐
│ Nginx Container (persistent)                    │
│  - Serves from /usr/share/nginx/html (volume)   │
│  - Listens on port 8080                         │
│  - Accessed by link checker container           │
└─────────────────────────────────────────────────┘
                    │
                    │ docker network
                    ↓
┌─────────────────────────────────────────────────┐
│ Link Checker Container (on-demand)              │
│  - Python + link checking code                  │
│  - Accesses nginx via http://docs-nginx:8080    │
│  - Outputs reports to mounted volume            │
└─────────────────────────────────────────────────┘
```

## Implementation Strategy

### Phase 1: Test MkDocs Site Creation

Deliverables:
- `tmp/test-mkdocs/` - minimal but complete test site
- `tmp/test-mkdocs/mkdocs.yml` - simplified config based on dyalog-docs
- `tmp/test-mkdocs/docs/` - sample markdown files with various link types
- Test content includes internal links, anchors, external links

Testing approach:
1. Create minimal site structure with Material theme
2. Include subset of plugins from dyalog-docs (search, privacy)
3. Include subset of markdown extensions (admonition, pymdownx features)
4. Create sample pages with various link types
5. Test build locally with `mkdocs build`
6. Verify output structure
7. Test serve with `mkdocs serve`

Success criteria:
- Site builds successfully with core plugins
- Generated HTML contains proper link structure
- Serves correctly with `mkdocs serve`
- Provides realistic test case for Docker setup

### Phase 2: Basic Nginx Container (Testable Standalone)

Deliverables:
- `docker/nginx/Dockerfile` - minimal nginx image
- `docker/nginx/nginx.conf` - basic serving configuration on port 8080
- `docker-compose.yml` - single service `docs-nginx`

Testing approach:
1. Use test site from Phase 1
2. Build test site to tmp/test-site-output (bind mount for this phase)
3. Mount output directory to nginx via bind mount
4. Verify can curl from host on port 8080
5. Verify can curl from another container using `docs-nginx:8080`
6. Measure response time baseline

Success criteria:
- Container starts successfully
- Can serve static content on port 8080
- Accessible via container name `docs-nginx`
- Sub-millisecond response over internal network

### Phase 3: MkDocs Builder Container (Testable Standalone)

Deliverables:
- `docker/mkdocs/Dockerfile` - Python + MkDocs + required plugins
- `docker/mkdocs/requirements.txt` - pinned dependencies
- Command that builds and exits with proper code

Required MkDocs plugins (from mkdocs.yml analysis):

For test site (Phase 1):
- mkdocs-material (theme)
- mkdocs-privacy-plugin
- pymdownx extensions (basic subset)

For full dyalog-docs (later):
- All above plus:
- mkdocs-macros-plugin
- mkdocs-monorepo-plugin (critical for site-of-sites)
- mkdocs-minify-plugin
- mkdocs-caption
- markdown-tables-extended

Testing approach:
1. Start with test site (simple plugins)
2. Mount test site read-only
3. Mount output directory as volume
4. Run build via service
5. Verify build completes without errors
6. Verify exit code is 0
7. Test intentional failure (break mkdocs.yml)
8. Verify non-zero exit code for failures
9. Time the build process
10. Graduate to dyalog-docs once working

Success criteria:
- Build completes successfully
- All plugins load correctly
- Exit code propagates properly (0 for success, non-zero for failure)
- Output directory contains valid HTML
- Can identify build time (baseline for cache investigation)

### Phase 4: Integration via Named Volume

Deliverables:
- Updated `docker-compose.yml` with named volume `site-output`
- Builder service that writes to volume at `/site`
- Nginx service that reads from same volume at `/usr/share/nginx/html`
- Dependency ordering (builder before nginx)

Testing approach:
1. Define `site-output` named volume
2. Configure builder to write to volume (`/site`)
3. Configure nginx to read from volume (`/usr/share/nginx/html:ro`)
4. Test build → serve workflow
5. Verify nginx serves built content (inspect volume with temp container)
6. Test rebuild scenario (volume cleanup)

Success criteria:
- Builder writes to shared volume
- Nginx serves content from shared volume (not bind mount)
- Can inspect volume contents via temporary container
- Can rebuild without manual volume cleanup
- No file permission issues

### Phase 5: Service-based Orchestration

Deliverables:
- `docker-compose.yml` with service-based builder
- Proper service dependencies (nginx depends_on builder)
- Health checks for nginx
- Exit code propagation from builder
- Documentation for workflow

Key design:
- Builder runs as service, builds once and exits
- Nginx waits for builder to complete successfully via `depends_on: condition: service_completed_successfully`
- Single command: `docker compose up docs-nginx`
- Builder failure prevents nginx startup

Testing approach:
1. Test cold start (no volumes exist)
2. Test warm start (volumes exist, rebuild)
3. Test builder failure propagation (intentional error in mkdocs.yml)
4. Verify nginx only starts after successful build
5. Add nginx readiness probe
6. Test full workflow end-to-end with `docker compose up docs-nginx`
7. Time each phase
8. Test rebuild: `docker compose down && docker compose up docs-nginx`
9. Test with dyalog-docs (full site with monorepo plugin)

Success criteria:
- Single command workflow: `docker compose up docs-nginx`
- Builder exit code propagates via depends_on condition
- Clear error messages if build fails
- Nginx waits for successful build before serving
- Can detect when site is ready for checking
- Rebuild workflow is clean and repeatable

### Phase 6: Build Cache Investigation

Deliverables:
- Performance measurements with/without cache
- Optional cache volume configuration
- Documentation of findings

Testing approach:
1. Measure full build time (Phase 5)
2. Research MkDocs caching mechanisms
3. Test with separate cache volume if applicable
4. Measure improvement (if any)
5. Document recommendation

Success criteria:
- Clear performance data
- Decision on whether caching is worth complexity
- Implementation only if significant improvement (>20%)

### Phase 7: Link Checker Integration (Future)

Deliverables (for context, not implementation):
- Link checker container definition
- Volume mount for report output
- Network configuration for internal access
- Command examples

This phase tests:
- Internal network connectivity
- Volume mounts for output
- Base URL configuration
- Performance over docker network

## File Structure

```
docker/
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── mkdocs/
│   ├── Dockerfile
│   └── requirements.txt
└── link-checker/          # Future
    ├── Dockerfile
    └── requirements.txt

tmp/
└── test-mkdocs/           # Test site for development
    ├── mkdocs.yml
    └── docs/
        ├── index.md
        ├── page1.md
        └── page2.md

docker-compose.yml
```

## Testing Strategy by Phase

### Phase 1 Tests (Test Site Creation)

```bash
# Create test site structure
mkdir -p tmp/test-mkdocs/docs

# Create mkdocs.yml (subset of dyalog-docs config)
cat > tmp/test-mkdocs/mkdocs.yml <<'EOF'
site_name: Test Documentation
theme:
  name: material
  features:
    - navigation.instant
    - navigation.tracking
plugins:
  - search
  - privacy
markdown_extensions:
  - admonition
  - pymdownx.superfences
  - pymdownx.details
  - toc:
      title: On this page
nav:
  - Home: index.md
  - Page 1: page1.md
  - Page 2: page2.md
EOF

# Create sample content with various link types
cat > tmp/test-mkdocs/docs/index.md <<'EOF'
# Test Documentation

Welcome to the test site.

- [Internal link to Page 1](page1.md)
- [Anchor link](#heading)
- [External link](https://www.example.com)

## Heading
EOF

cat > tmp/test-mkdocs/docs/page1.md <<'EOF'
# Page 1

Link back to [home](index.md).
Link to [Page 2](page2.md).
Link to [anchor on Page 2](page2.md#section).
EOF

cat > tmp/test-mkdocs/docs/page2.md <<'EOF'
# Page 2

## Section

Content here.
EOF

# Test local build
cd tmp/test-mkdocs
mkdocs build
mkdocs serve

# Verify in browser: http://localhost:8000
# Test all links work
# Check exit codes
```

### Phase 2 Tests (Nginx Container)

```bash
# First build test site from Phase 1 to a bind-mounted directory
cd tmp/test-mkdocs
mkdocs build --site-dir ../test-site-output
cd ../..

# Build nginx image
docker compose build docs-nginx

# Start nginx (compose mounts tmp/test-site-output for this phase)
docker compose up docs-nginx

# Test from host
curl http://localhost:8080

# Test from another container
docker run --rm --network link_check_default curlimages/curl curl http://docs-nginx:8080

# Measure response time
time curl http://localhost:8080 > /dev/null
```

### Phase 3 Tests (Builder Container)

```bash
# Build mkdocs image
docker compose build mkdocs-builder

# Test with test site (writes to named volume)
docker compose run --rm mkdocs-builder

# Verify output exists in volume (can't ls directly)
# Instead, verify via container inspection
docker compose run --rm mkdocs-builder ls -la /site/

# Or mount volume to temporary container to inspect
docker run --rm -v link_check_site-output:/site alpine ls -la /site/

# Check for errors in build log

# Test exit code propagation
docker compose run --rm mkdocs-builder
echo $?  # Should be 0 for success

# Test with broken config (introduce error in mkdocs.yml)
# Verify non-zero exit code
docker compose run --rm mkdocs-builder
echo $?  # Should be non-zero for failure
```

### Phase 4 Tests (Named Volume)

```bash
# Clean start
docker compose down -v

# Build and verify volume
docker compose run --rm mkdocs-builder
docker volume ls | grep site-output

# Inspect volume contents
docker run --rm -v link_check_site-output:/site alpine ls -la /site/

# Start nginx (now reading from named volume, not bind mount)
docker compose up -d docs-nginx

# Verify serving
curl http://localhost:8080

# Rebuild test
docker compose run --rm mkdocs-builder
# Verify nginx serves updated content (may need restart)
curl http://localhost:8080 | grep -i "updated content marker"
```

### Phase 5 Tests (Service-based Orchestration)

```bash
# Full workflow test - single command
docker compose down -v
docker compose up docs-nginx

# Should see:
# 1. Builder container starts
# 2. Builder runs mkdocs build
# 3. Builder exits with code 0
# 4. Nginx starts and serves content

# Verify content served
curl http://localhost:8080 | grep "Test Documentation"

# Test failure propagation
# Introduce error in mkdocs.yml (invalid syntax)
docker compose down -v
docker compose up docs-nginx
# Should fail to start nginx, show builder error

# Fix mkdocs.yml
# Test rebuild
docker compose down
docker compose up docs-nginx

# Timing test
time docker compose up docs-nginx

# Test with dyalog-docs (full site)
# Modify compose to mount dyalog-docs instead of test-mkdocs
# Update requirements.txt with all plugins
docker compose down -v
docker compose up docs-nginx
# Measure build time
```

### Phase 6 Tests (Build Cache)

```bash
# Measure baseline (from Phase 5)
docker compose down -v
time docker compose up docs-nginx

# Research MkDocs caching
# Add cache volume if applicable
# Measure improvement

# Compare times
# Document findings
```

## Dockerfile Sketches

### nginx/Dockerfile

```dockerfile
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Site content comes from volume mount
# No COPY of site files

EXPOSE 8080
```

### nginx/nginx.conf (sketch)

```nginx
server {
    listen 8080;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### mkdocs/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /build

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source docs come from volume mount
# Build output goes to volume mount

# Default command builds the site
# Exit code propagates naturally
CMD ["mkdocs", "build", "--clean", "--site-dir", "/site"]
```

### mkdocs/requirements.txt (initial)

```
mkdocs>=1.5.0
mkdocs-material>=9.5.0
```

For full dyalog-docs support, add:
```
mkdocs-macros-plugin
mkdocs-monorepo-plugin
mkdocs-minify-plugin
mkdocs-caption
markdown-tables-extended
pymdown-extensions
```

## Docker Compose Sketch

```yaml
services:
  mkdocs-builder:
    build:
      context: docker/mkdocs
    volumes:
      - ./tmp/test-mkdocs:/docs:ro  # Start with test site
      - site-output:/site
    working_dir: /docs
    # Command in Dockerfile CMD: mkdocs build --clean --site-dir /site
    # Exit code propagates naturally

  docs-nginx:
    build:
      context: docker/nginx
    container_name: docs-nginx
    ports:
      - "8080:8080"
    volumes:
      - site-output:/usr/share/nginx/html:ro  # Read from shared named volume
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080/"]
      interval: 5s
      timeout: 3s
      retries: 3
    depends_on:
      mkdocs-builder:
        condition: service_completed_successfully  # Critical: wait for successful build
    # Nginx only starts if builder exits 0

volumes:
  site-output:  # Shared named volume for build artifacts
```

## Decisions Made

1. **Builder as service**: Use service with `depends_on: condition: service_completed_successfully`
   - Single command: `docker compose up docs-nginx`
   - Exit code propagation built-in

2. **Build failures**: Exit code propagates via depends_on condition
   - Builder exits non-zero → nginx doesn't start
   - Clear error in compose output

3. **Port exposure**: 8080 consistently
   - Host access: `http://localhost:8080`
   - Internal access: `http://docs-nginx:8080`
   - No port 80 anywhere

4. **Volume cleanup**: Manual `docker compose down -v` for fresh builds
   - Rebuild without cleanup: `docker compose down && docker compose up docs-nginx`

5. **MkDocs configuration**:
   - Phase 1: Create test site (tmp/test-mkdocs)
   - Later phases: Switch to dyalog-docs
   - Test site provides fast iteration

6. **Dependencies**: Pin versions in requirements.txt
   - Extract from working dyalog-docs build if available
   - Or use latest stable versions
   - Required plugins identified from mkdocs.yml

7. **Build caching**: Investigate in Phase 6
   - Measure build time with/without cache
   - Add cache volume only if significant improvement
   - Not blocking for initial implementation

## MkDocs Requirements Investigation

Based on dyalog-docs/mkdocs.yml analysis:

**Plugins used:**
- privacy
- search
- macros
- monorepo (critical for site-of-sites)
- minify
- caption

**Markdown extensions:**
- admonition
- pymdownx.details
- pymdownx.keys
- pymdownx.superfences
- pymdownx.arithmatex
- pymdownx.highlight
- attr_list
- abbr
- footnotes
- md_in_html
- markdown_tables_extended
- toc

**Theme:**
- material with Be Vietnam Pro font

**PyPI package names to verify:**
- mkdocs-material
- mkdocs-privacy-plugin (or mkdocs-privacy)
- mkdocs-macros-plugin
- mkdocs-monorepo-plugin
- mkdocs-minify-plugin
- mkdocs-caption
- markdown-tables-extended (or pymdown-extensions might include this)
- pymdown-extensions (NOTE: pymdown, not pymdownx)

## Risk Mitigation

### Risk: MkDocs plugins incompatible
Mitigation: Test with minimal config first (Phase 1), add plugins incrementally

### Risk: Monorepo plugin requires special handling
Mitigation: Review plugin docs, test with single sub-site first, then full monorepo

### Risk: Build too slow in Docker
Mitigation: Use BuildKit, measure at each phase, Phase 6 investigates caching

### Risk: Volume permissions issues
Mitigation: Run containers as non-root where possible, test volume permissions

### Risk: Nginx serves stale content after rebuild
Mitigation: Health check strategy, volume mount options, test rebuild workflow

### Risk: Plugin package names differ from config names
Mitigation: Research correct PyPI names, test incrementally

## Performance Targets

- Test site build: < 10 seconds
- Full dyalog-docs build: < 5 minutes (baseline to improve in Phase 6)
- Nginx response time: < 10ms over internal network
- Container startup: < 5 seconds
- Volume mount overhead: negligible vs native filesystem

## Success Criteria (Overall)

1. Can build MkDocs site from mounted source
2. Can serve via nginx from shared volume on port 8080
3. Single command workflow: `docker compose up docs-nginx`
4. Exit code propagation works correctly
5. Workflow is repeatable and documented
6. Each phase independently testable
7. Clear error messages for common failures
8. Ready for link checker integration (Phase 7)

## Next Steps After Plan Approval

1. Create branch for work
2. Implement Phase 1: Create test MkDocs site with sample links
3. Validate Phase 1 locally before proceeding
4. Implement Phase 2: Basic nginx container with test site
5. Implement Phase 3: MkDocs builder container with exit code tests
6. Implement Phase 4: Named volume integration
7. Implement Phase 5: Service-based orchestration with `docker compose up docs-nginx`
8. Validate Phases 2-5 work together
9. Test with full dyalog-docs site
10. Implement Phase 6: Investigate build caching if needed
11. Document findings and workflow
12. Prepare for Phase 7: Link checker integration
