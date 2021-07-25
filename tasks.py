from pathlib import Path

import invoke

PROJECT_ROOT = Path(__file__).parent


# -------
# Linting
# -------


@invoke.task(aliases=["lint"])
def lint_all(ctx, fix=False):
    """
    Run all linting tasks.
    """
    lint_isort(ctx, fix=fix)
    lint_black(ctx, fix=fix)
    lint_flake8(ctx)
    lint_mypy(ctx)
    lint_bandit(ctx)
    lint_django_doctor(ctx)
    lint_poetry_check(ctx)


@invoke.task
def lint_isort(ctx, fix=False):
    if fix:
        print(">>> sorting imports...")
        with ctx.cd(PROJECT_ROOT / "src"):
            ctx.run("isort .", pty=True)
    else:
        print(">>> checking imports...")
        with ctx.cd(PROJECT_ROOT / "src"):
            ctx.run("isort --check-only .", pty=True)


@invoke.task
def lint_black(ctx, fix=False):
    if fix:
        print(">>> auto-formatting...")
        with ctx.cd(PROJECT_ROOT / "src"):
            ctx.run("black .", pty=True)
    else:
        print(">>> checking formatting...")
        with ctx.cd(PROJECT_ROOT / "src"):
            ctx.run("black --check .", pty=True)


@invoke.task
def lint_flake8(ctx):
    print(">>> linting...")
    with ctx.cd(PROJECT_ROOT / "src"):
        ctx.run("flake8", pty=True)


@invoke.task
def lint_mypy(ctx):
    print(">>> type-checking...")
    with ctx.cd(PROJECT_ROOT / "src"):
        ctx.run("mypy .", pty=True)


@invoke.task
def lint_bandit(ctx):
    print(">>> checking for security issues...")
    with ctx.cd(PROJECT_ROOT):
        ctx.run("bandit -r src/katubi", pty=True)


@invoke.task
def lint_django_doctor(ctx):
    print(">>> checking Django...")
    with ctx.cd(PROJECT_ROOT):
        ctx.run("django_doctor check", pty=True)


@invoke.task
def lint_poetry_check(ctx):
    print(">>> checking pyproject.toml...")
    ctx.run("poetry check", pty=True)


# -------
# Testing
# -------


@invoke.task(aliases=["test"])
def test_all(ctx):
    """
    Run all tests.
    """
    _run_tests(ctx)


@invoke.task
def test_unit(ctx):
    _run_tests(ctx, "tests/unit")


@invoke.task
def test_integration(ctx):
    _run_tests(ctx, "tests/integration")


@invoke.task
def test_functional(ctx):
    _run_tests(ctx, "tests/functional")


def _run_tests(ctx, path: str = ""):
    with ctx.cd(PROJECT_ROOT / "src"):
        ctx.run(
            f"pytest {path}",
            pty=True,
        )
