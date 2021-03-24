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
    test_unit(ctx)
    test_integration(ctx)
    test_functional(ctx)


@invoke.task
def test_unit(ctx):
    with ctx.cd(PROJECT_ROOT / "src"):
        ctx.run("pytest tests/unit", pty=True)


@invoke.task
def test_integration(ctx):
    with ctx.cd(PROJECT_ROOT / "src"):
        ctx.run("pytest tests/integration", pty=True)


@invoke.task
def test_functional(ctx):
    with ctx.cd(PROJECT_ROOT / "src"):
        ctx.run("pytest tests/functional", pty=True)
