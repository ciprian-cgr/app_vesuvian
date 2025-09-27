#!/usr/bin/env bash
set -euo pipefail

# migrate_to_domains.sh
# Creates a domain-oriented folder layout and moves existing frontend files.
# Intended for the 'frontend' folder of the project.
# Usage:
#   cd frontend
#   ./scripts/migrate_to_domains.sh
# The script will use `git mv` when run inside a git repo, otherwise it will fall
# back to plain `mv`. It is written to be safe / idempotent: existing target files
# will be skipped.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

USING_GIT=false
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  USING_GIT=true
fi

do_move() {
  local src="$1"
  local dst="$2"

  if [ ! -e "$src" ]; then
    echo "SKIP: source not found: $src"
    return 0
  fi

  if [ -e "$dst" ]; then
    echo "SKIP: destination already exists: $dst"
    return 0
  fi

  mkdir -p "$(dirname "$dst")"

  if [ "$USING_GIT" = true ]; then
    echo "git mv: $src -> $dst"
    git mv --force "$src" "$dst"
  else
    echo "mv: $src -> $dst"
    mv "$src" "$dst"
  fi
}

# Directory creation (in bulk to be explicit)
mkdir -p src/domains/users/auth
mkdir -p src/domains/users/components
mkdir -p src/domains/users/pages
mkdir -p src/shared/layout
mkdir -p src/shared/ui
mkdir -p src/shared/lib
mkdir -p src/shared/hooks
mkdir -p src/shared/types
mkdir -p src/shared/utils

# Files to move: list of pairs: source -> destination
declare -a MOVES=(
  "src/auth/AuthContext.tsx|src/domains/users/auth/AuthContext.tsx"
  "src/SignInForm.tsx|src/domains/users/components/SignInForm.tsx"
  "src/SignOutButton.tsx|src/domains/users/components/SignOutButton.tsx"
  "src/components/pages/Settings.tsx|src/domains/users/pages/Settings.tsx"
  "src/components/pages/Dashboard.tsx|src/domains/users/pages/Dashboard.tsx"

  "src/components/layout/Layout.tsx|src/shared/layout/Layout.tsx"
  "src/components/layout/Navigation.tsx|src/shared/layout/Navigation.tsx"

  "src/components/ui/Button.tsx|src/shared/ui/Button.tsx"
  "src/components/ui/Card.tsx|src/shared/ui/Card.tsx"
  "src/components/ui/Input.tsx|src/shared/ui/Input.tsx"
  "src/components/ui/Select.tsx|src/shared/ui/Select.tsx"
  "src/components/ui/LoadingSpinner.tsx|src/shared/ui/LoadingSpinner.tsx"
  "src/components/ui/ErrorMessage.tsx|src/shared/ui/ErrorMessage.tsx"

  "src/lib/api.ts|src/shared/lib/api.ts"
  "src/lib/utils.ts|src/shared/lib/utils.ts"

  "src/hooks/useDebounce.ts|src/shared/hooks/useDebounce.ts"
  "src/hooks/useLocalStorage.ts|src/shared/hooks/useLocalStorage.ts"

  "src/types/index.ts|src/shared/types/index.ts"

  "src/utils/constants.ts|src/shared/utils/constants.ts"
  "src/utils/formatters.ts|src/shared/utils/formatters.ts"
  "src/utils/validation.ts|src/shared/utils/validation.ts"
)

echo "Starting file moves (using git mv=$USING_GIT)..."

for pair in "${MOVES[@]}"; do
  IFS='|' read -r src dst <<< "$pair"
  do_move "$src" "$dst"
done

# Post-move: suggest re-checking imports
cat <<'EOF'

Migration complete (file moves attempted).
Next steps:
  1) Update import paths across the codebase to point to the new locations (or create re-export adapters in the old paths).
  2) Run TypeScript check and a build to catch broken imports:
       npx tsc -p . --noEmit
       npm run build
  3) If using git, review the staged changes and commit them.

If you want, I can now update imports automatically to reflect the new paths.
EOF

exit 0
