# Codex Prompt — Create Public GitHub Repo in `heurema`

You are working in a local shell environment with Git and GitHub CLI (`gh`) installed and authenticated.

Goal: unpack the documentation archive, initialize a Git repository, create a public GitHub repository under the `heurema` organization, and push the contents.

Repository:

```text
heurema/cak
```

Archive file name:

```text
cak-docs.zip
```

## Requirements

1. Unpack the archive.
2. Validate the directory structure.
3. Run `python3 scripts/check_docs.py`.
4. Initialize a Git repo.
5. Create a public GitHub repo in the `heurema` organization.
6. Push the repo to GitHub.
7. If the repo already exists, do not destroy it. Stop and report that `heurema/cak` already exists.
8. Do not force-push.
9. Do not commit secrets, `.env` files, private keys, credentials, tokens, local caches, or generated build output.

## Commands

```bash
set -euo pipefail

ARCHIVE="${ARCHIVE:-cak-docs.zip}"
REPO_DIR="cak"
ORG="heurema"
REPO_NAME="cak"
REMOTE="$ORG/$REPO_NAME"

# 1. Verify GitHub CLI auth.
gh auth status

# 2. Ensure the target repo does not already exist.
if gh repo view "$REMOTE" >/dev/null 2>&1; then
  echo "Repository $REMOTE already exists. Stop to avoid overwrite."
  exit 1
fi

# 3. Prepare workspace.
rm -rf "$REPO_DIR"
mkdir "$REPO_DIR"

# 4. Unpack archive.
unzip "$ARCHIVE" -d "$REPO_DIR"

# If the archive contains a top-level cak directory, move into it.
if [ -d "$REPO_DIR/cak" ]; then
  tmp_dir="${REPO_DIR}__tmp"
  mv "$REPO_DIR/cak" "$tmp_dir"
  rm -rf "$REPO_DIR"
  mv "$tmp_dir" "$REPO_DIR"
fi

cd "$REPO_DIR"

# 5. Safety scan.
if find . \( -name ".env" -o -name ".env.*" -o -name "*.pem" -o -name "*.key" -o -name "*.p12" \) | grep -q .; then
  echo "Potential secret files detected. Stop before commit."
  find . \( -name ".env" -o -name ".env.*" -o -name "*.pem" -o -name "*.key" -o -name "*.p12" \)
  exit 1
fi

# 6. Validate docs.
python3 scripts/check_docs.py

# 7. Initialize git repo.
git init
git branch -M main
git add .
git status
git commit -m "Initial CAK documentation"

# 8. Create public repo and push.
gh repo create "$REMOTE"   --public   --description "CAK: typed semantic control layer for AI-agent behavior, learning, replay, governance, portability, and cost control."   --source=.   --remote=origin   --push

# 9. Add topics where supported.
gh repo edit "$REMOTE"   --add-topic ai-agents   --add-topic agent-runtime   --add-topic governance   --add-topic agent-language   --add-topic causal-ai   --add-topic replay   --add-topic agent-safety || true

# 10. Final report.
echo "Published: https://github.com/$REMOTE"
echo "Commit: $(git rev-parse HEAD)"
```

After completion, report:

- remote URL;
- commit hash;
- whether docs check passed;
- whether any warnings appeared.
```
