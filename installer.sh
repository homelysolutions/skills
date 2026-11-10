#!/usr/bin/env bash
# Install the skills of this repository.
#   ./installer.sh            -> every skill into ~/.claude/skills (all your projects)
#   ./installer.sh <project>  -> every skill into <project>/.claude/skills
#   ./installer.sh <project> ponytail impeccable -> only the named skills
# Existing skills with the same name are replaced. claude-seo is a plugin: see README.md.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
if [ $# -ge 1 ] && [ -d "$1" ]; then
  target="$1/.claude/skills"; shift
else
  target="$HOME/.claude/skills"
fi
mkdir -p "$target"
names=("$@")
if [ ${#names[@]} -eq 0 ]; then
  for d in "$here"/skills/*/; do names+=("$(basename "$d")"); done
fi
for n in "${names[@]}"; do
  src="$here/skills/$n"
  [ -f "$src/SKILL.md" ] || { echo "Skill inconnu : $n" >&2; exit 1; }
  rm -rf "${target:?}/$n"
  cp -R "$src" "$target/$n"
  echo "installé : $n"
done
echo "-> $target"
