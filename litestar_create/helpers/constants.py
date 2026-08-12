LITESTAR_COLOR = "#edb641"

TEMPLATES_REPO = "litestar-org/litestar-templates"
TEMPLATES_BRANCH = "main"
REQUEST_TIMEOUT = 30

MANIFEST_URL = f"https://raw.githubusercontent.com/{TEMPLATES_REPO}/{TEMPLATES_BRANCH}/templates.json"
TARBALL_URL = (
    f"https://codeload.github.com/{TEMPLATES_REPO}/tar.gz/refs/heads/{TEMPLATES_BRANCH}"
)
# GitHub names the archive folder after the repository, without the owner
ARCHIVE_ROOT = f"{TEMPLATES_REPO.split('/')[-1]}-{TEMPLATES_BRANCH}"
