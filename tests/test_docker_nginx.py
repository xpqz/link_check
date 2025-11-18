"""Tests for nginx Docker container setup and functionality.

This test module verifies Phase 2 requirements:
- Nginx Dockerfile builds successfully
- Nginx configuration is valid
- Test site builds to bind mount directory
- Docker compose configuration is valid
- Nginx serves content from host on port 8080
- Nginx is accessible from other containers via name resolution
- Response times meet baseline requirements
"""

import subprocess
import time
import pytest
from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).parent.parent
DOCKER_NGINX_DIR = PROJECT_ROOT / "docker" / "nginx"
TEST_SITE_OUTPUT = PROJECT_ROOT / "tmp" / "test-site-output"
TEST_MKDOCS_DIR = PROJECT_ROOT / "tmp" / "test-mkdocs"
DOCKER_COMPOSE_FILE = PROJECT_ROOT / "docker-compose.yml"
RUN_DOCKER_TESTS = os.getenv("RUN_DOCKER_TESTS") == "1"
docker_required = pytest.mark.skipif(
    not RUN_DOCKER_TESTS,
    reason="Requires Docker; set RUN_DOCKER_TESTS=1 to enable",
)


def run_command(cmd, cwd=None, check=True, capture_output=True, timeout=30):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        timeout=timeout,
        check=check,
    )
    return result


class TestNginxDockerfile:
    """Tests for nginx Dockerfile creation and building."""

    def test_nginx_directory_exists(self):
        """Verify docker/nginx/ directory exists."""
        assert DOCKER_NGINX_DIR.exists(), f"Directory {DOCKER_NGINX_DIR} does not exist"
        assert DOCKER_NGINX_DIR.is_dir(), f"{DOCKER_NGINX_DIR} is not a directory"

    def test_nginx_dockerfile_exists(self):
        """Verify docker/nginx/Dockerfile exists."""
        dockerfile = DOCKER_NGINX_DIR / "Dockerfile"
        assert dockerfile.exists(), f"Dockerfile does not exist at {dockerfile}"
        assert dockerfile.is_file(), f"{dockerfile} is not a file"

    def test_nginx_dockerfile_content(self):
        """Verify Dockerfile has required directives."""
        dockerfile = DOCKER_NGINX_DIR / "Dockerfile"
        content = dockerfile.read_text()

        # Check for nginx:alpine base image
        assert (
            "FROM nginx:alpine" in content
        ), "Dockerfile must use nginx:alpine base image"

        # Check for EXPOSE 8080
        assert "EXPOSE 8080" in content, "Dockerfile must expose port 8080"

    @docker_required
    def test_nginx_dockerfile_builds(self):
        """Verify Dockerfile builds successfully."""
        result = run_command(
            "docker build -t test-nginx docker/nginx/",
            cwd=PROJECT_ROOT,
            timeout=120,
        )
        assert result.returncode == 0, f"Docker build failed: {result.stderr}"
        assert "Successfully tagged test-nginx" in result.stdout or result.stderr


class TestNginxConfiguration:
    """Tests for nginx configuration file."""

    def test_nginx_config_exists(self):
        """Verify nginx.conf exists."""
        config_file = DOCKER_NGINX_DIR / "nginx.conf"
        assert config_file.exists(), f"nginx.conf does not exist at {config_file}"
        assert config_file.is_file(), f"{config_file} is not a file"

    def test_nginx_config_content(self):
        """Verify nginx.conf has required configuration."""
        config_file = DOCKER_NGINX_DIR / "nginx.conf"
        content = config_file.read_text()

        # Check for port 8080 listener
        assert (
            "listen 8080" in content or "listen       8080" in content
        ), "nginx.conf must listen on port 8080"

        # Check for root directory
        assert (
            "/usr/share/nginx/html" in content
        ), "nginx.conf must set root to /usr/share/nginx/html"

        # Check for index file
        assert "index.html" in content, "nginx.conf must specify index.html"

        # Check for try_files directive
        assert "try_files" in content, "nginx.conf must include try_files directive"

    @docker_required
    def test_nginx_config_syntax_valid(self):
        """Verify nginx configuration syntax is valid."""
        config_file = DOCKER_NGINX_DIR / "nginx.conf"
        cmd = f"docker run --rm -v {config_file}:/etc/nginx/nginx.conf:ro nginx:alpine nginx -t"
        result = run_command(cmd, timeout=30)

        assert (
            result.returncode == 0
        ), f"nginx config validation failed: {result.stderr}"
        assert "syntax is ok" in result.stderr or "successful" in result.stderr


class TestSiteBuild:
    """Tests for building test site to bind mount directory."""

    def test_test_site_output_directory_exists(self):
        """Verify tmp/test-site-output/ directory can be created."""
        # Create directory if it doesn't exist (needed for CI)
        TEST_SITE_OUTPUT.mkdir(parents=True, exist_ok=True)
        assert TEST_SITE_OUTPUT.exists(), f"Directory {TEST_SITE_OUTPUT} does not exist"
        assert TEST_SITE_OUTPUT.is_dir(), f"{TEST_SITE_OUTPUT} is not a directory"

    def test_mkdocs_builds_to_test_site_output(self):
        """Verify mkdocs builds successfully to test-site-output."""
        # Ensure parent directory exists
        TEST_SITE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        # Clean output directory first
        if TEST_SITE_OUTPUT.exists():
            run_command(f"rm -rf {TEST_SITE_OUTPUT}/*")

        # Build site
        result = run_command(
            "mkdocs build --site-dir ../test-site-output",
            cwd=TEST_MKDOCS_DIR,
            timeout=60,
        )

        assert result.returncode == 0, f"mkdocs build failed: {result.stderr}"
        assert TEST_SITE_OUTPUT.exists(), "Output directory not created"

    def test_built_site_has_html_files(self):
        """Verify built site contains expected HTML files."""
        index_html = TEST_SITE_OUTPUT / "index.html"
        assert index_html.exists(), "index.html not found in built site"

        page1_html = TEST_SITE_OUTPUT / "page1" / "index.html"
        assert page1_html.exists(), "page1/index.html not found in built site"

        page2_html = TEST_SITE_OUTPUT / "page2" / "index.html"
        assert page2_html.exists(), "page2/index.html not found in built site"


@docker_required
class TestDockerCompose:
    """Tests for docker-compose.yml configuration."""

    def test_docker_compose_file_exists(self):
        """Verify docker-compose.yml exists."""
        assert (
            DOCKER_COMPOSE_FILE.exists()
        ), f"docker-compose.yml does not exist at {DOCKER_COMPOSE_FILE}"
        assert DOCKER_COMPOSE_FILE.is_file(), f"{DOCKER_COMPOSE_FILE} is not a file"

    def test_docker_compose_syntax_valid(self):
        """Verify docker-compose.yml syntax is valid."""
        result = run_command("docker compose config", cwd=PROJECT_ROOT, timeout=30)
        assert (
            result.returncode == 0
        ), f"docker-compose.yml validation failed: {result.stderr}"

    def test_docker_compose_defines_nginx_service(self):
        """Verify docker-compose.yml defines docs-nginx service."""
        result = run_command("docker compose config", cwd=PROJECT_ROOT)
        output = result.stdout

        assert "docs-nginx" in output, "docs-nginx service not defined"

    def test_nginx_service_configuration(self):
        """Verify docs-nginx service has correct configuration."""
        result = run_command("docker compose config", cwd=PROJECT_ROOT)
        output = result.stdout

        # Check container name
        assert (
            "container_name: docs-nginx" in output
            or 'container_name: "docs-nginx"' in output
        ), "Container name must be set to docs-nginx"

        # Check port mapping
        assert "target: 8080" in output, "Port target 8080 not found"
        assert (
            'published: "8080"' in output or "published: 8080" in output
        ), "Published port 8080 not found"

        # Check volume mount
        assert (
            "/usr/share/nginx/html" in output
        ), "Volume mount to /usr/share/nginx/html not found"
        assert (
            "test-site-output" in output
        ), "Volume mount from test-site-output not found"


@docker_required
class TestNginxFromHost:
    """Tests for nginx container accessibility from host."""

    @pytest.fixture(scope="class")
    def nginx_container(self):
        """Start nginx container for testing."""
        # Ensure test site is built
        if not (TEST_SITE_OUTPUT / "index.html").exists():
            run_command(
                "mkdocs build --site-dir ../test-site-output",
                cwd=TEST_MKDOCS_DIR,
            )

        # Start container
        run_command(
            "docker compose up -d docs-nginx",
            cwd=PROJECT_ROOT,
            timeout=60,
        )

        # Wait for container to be ready
        time.sleep(2)

        yield

        # Cleanup
        run_command("docker compose down", cwd=PROJECT_ROOT)

    def test_nginx_container_starts(self, nginx_container):
        """Verify nginx container starts without errors."""
        result = run_command("docker compose ps docs-nginx", cwd=PROJECT_ROOT)
        assert result.returncode == 0
        assert "docs-nginx" in result.stdout
        # Container should be running (not exited)
        assert "Up" in result.stdout or "running" in result.stdout.lower()

    def test_nginx_serves_index_from_host(self, nginx_container):
        """Verify nginx serves index.html from host."""
        result = run_command("curl -s http://localhost:8080", timeout=10)
        assert result.returncode == 0, f"curl failed: {result.stderr}"
        assert len(result.stdout) > 0, "Empty response from nginx"
        assert "<html" in result.stdout.lower(), "Response is not HTML"

    def test_nginx_serves_page1_from_host(self, nginx_container):
        """Verify nginx serves page1 from host."""
        result = run_command("curl -s http://localhost:8080/page1/", timeout=10)
        assert result.returncode == 0, f"curl failed: {result.stderr}"
        assert len(result.stdout) > 0, "Empty response from nginx"
        assert "<html" in result.stdout.lower(), "Response is not HTML"

    def test_nginx_http_status_code(self, nginx_container):
        """Verify nginx returns 200 OK status."""
        result = run_command(
            "curl -s -o /dev/null -w '%{http_code}' http://localhost:8080",
            timeout=10,
        )
        assert result.returncode == 0
        assert (
            result.stdout.strip() == "200"
        ), f"Expected status 200, got {result.stdout.strip()}"


@docker_required
class TestNginxFromContainer:
    """Tests for nginx container accessibility from other containers."""

    @pytest.fixture(scope="class")
    def nginx_running(self):
        """Ensure nginx is running."""
        # Ensure test site is built
        if not (TEST_SITE_OUTPUT / "index.html").exists():
            run_command(
                "mkdocs build --site-dir ../test-site-output",
                cwd=TEST_MKDOCS_DIR,
            )

        # Start container in detached mode
        run_command(
            "docker compose up -d docs-nginx",
            cwd=PROJECT_ROOT,
            timeout=60,
        )

        # Wait for container to be ready
        time.sleep(2)

        yield

        # Cleanup
        run_command("docker compose down", cwd=PROJECT_ROOT)

    def test_nginx_accessible_by_container_name(self, nginx_running):
        """Verify nginx is accessible from another container using container name."""
        # Get the network name (should be link_check_default)
        result = run_command(
            "docker network ls --filter name=link_check --format '{{.Name}}'",
            timeout=10,
        )
        networks = result.stdout.strip().split("\n")
        network = (
            [n for n in networks if "default" in n][0]
            if networks
            else "link_check_default"
        )

        # Run curl from another container
        cmd = f"docker run --rm --network {network} curlimages/curl:latest curl -s http://docs-nginx:8080"
        result = run_command(cmd, timeout=30)

        assert result.returncode == 0, f"curl from container failed: {result.stderr}"
        assert len(result.stdout) > 0, "Empty response from nginx"
        assert "<html" in result.stdout.lower(), "Response is not HTML"


@docker_required
class TestNginxPerformance:
    """Tests for nginx response time baseline."""

    @pytest.fixture(scope="class")
    def nginx_running(self):
        """Ensure nginx is running."""
        # Ensure test site is built
        if not (TEST_SITE_OUTPUT / "index.html").exists():
            run_command(
                "mkdocs build --site-dir ../test-site-output",
                cwd=TEST_MKDOCS_DIR,
            )

        # Start container
        run_command(
            "docker compose up -d docs-nginx",
            cwd=PROJECT_ROOT,
            timeout=60,
        )

        # Wait for container to be ready
        time.sleep(2)

        yield

        # Cleanup
        run_command("docker compose down", cwd=PROJECT_ROOT)

    def test_nginx_response_time_baseline(self, nginx_running):
        """Measure and verify nginx response time meets baseline."""
        response_times = []

        # Warm up
        run_command("curl -s http://localhost:8080 > /dev/null", timeout=10)

        # Measure 5 requests
        for _ in range(5):
            start = time.time()
            result = run_command(
                "curl -s http://localhost:8080 > /dev/null", timeout=10
            )
            elapsed = time.time() - start

            assert result.returncode == 0, "curl failed"
            response_times.append(elapsed)

        avg_time = sum(response_times) / len(response_times)

        # Log the baseline for documentation
        print(
            f"\nNginx response time baseline: {avg_time*1000:.2f}ms (avg of 5 requests)"
        )
        print(f"Individual times: {[f'{t*1000:.2f}ms' for t in response_times]}")

        # Verify reasonable response time (should be well under 100ms from host)
        assert (
            avg_time < 0.1
        ), f"Average response time {avg_time*1000:.2f}ms exceeds 100ms threshold"
