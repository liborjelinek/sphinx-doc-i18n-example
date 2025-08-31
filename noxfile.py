import nox

# Speed up builds by uv and reusing virtualenvs
nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "uv"


@nox.session
@nox.parametrize("language", ["cs", "uk"])
def gettext(session, language):
    """Generate .pot files and update .po files."""
    session.install("sphinx==8.1.3", "sphinx-intl==2.3.2")

    # Generate .pot files from Sphinx
    session.run("sphinx-build", "-b", "gettext", "source", "build/gettext")

    # Update .po from .pot templates
    session.run(
        "sphinx-intl",
        "update",  # update .po files
        "-p",  # from .pot files at
        "build/gettext",
        "-l",  # for language
        language,
        # No line wrapping
        "-w",
        "0",
    )


@nox.session
@nox.parametrize("language", ["en", "cs", "uk"])
def build(session, language):
    """Build documentation for a language."""
    session.install("sphinx==8.1.3")
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-D",
        f"language={language}",
        "source",
        f"build/{language}",
    )
