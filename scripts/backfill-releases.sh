#!/usr/bin/env bash
# Backfill releases for upstream xremap versions newer than the packaged version.
#
# For each missing version (oldest -> newest) this script:
#   1. Updates xremap.spec (Version, Release reset to 1, %changelog entry),
#      commits and pushes to master.
#   2. Creates the GitHub release v<version>, which triggers the rpm workflow.
#   3. Waits for the rpm workflow run to succeed before moving to the next
#      version (COPR builds must land in version order, and the submit job
#      waits for the COPR build to finish).
#
# Requirements: gh (authenticated), git push access, a clean checkout of master.
#
# Usage: ./scripts/backfill-releases.sh

set -euo pipefail

repo="BlakeGardner/xremap-fedora"
upstream_repo="xremap/xremap"

branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" != "master" ]; then
    echo "Error: run this from the master branch (currently on $branch)." >&2
    exit 1
fi
if [ -n "$(git status --porcelain)" ]; then
    echo "Error: working tree is not clean." >&2
    exit 1
fi
git pull --ff-only

current=$(awk '/^Version:/ {print $2}' xremap.spec)
echo "Current packaged version: $current"

latest=$(gh api "repos/$upstream_repo/releases/latest" --jq '.tag_name')
latest="${latest#v}"
echo "Latest upstream version: $latest"

# Upstream stable versions newer than the current one, oldest first, capped at
# the release upstream marks as latest (ignores stray tags that sort above it).
mapfile -t missing < <(
    gh api "repos/$upstream_repo/releases?per_page=100" \
        --jq '.[] | select(.draft == false and .prerelease == false) | .tag_name' |
        sed 's/^v//' |
        sort -V |
        awk -v cur="$current" -v latest="$latest" '
            found && !done { print }
            $0 == cur { found = 1 }
            $0 == latest { done = 1 }
        '
)

if [ "${#missing[@]}" -eq 0 ]; then
    echo "No missing versions — nothing to backfill."
    exit 0
fi

echo "Versions to backfill (${#missing[@]}): ${missing[*]}"

for version in "${missing[@]}"; do
    echo
    echo "=== Backfilling $version ==="

    if gh release view "v$version" --repo "$repo" > /dev/null 2>&1; then
        echo "Release v$version already exists — skipping."
        continue
    fi

    # Skip the spec bump if a previous run already pushed it before failing.
    if [ "$(awk '/^Version:/ {print $2}' xremap.spec)" != "$version" ]; then
        ./scripts/update-spec-version.sh "$version"
        git add xremap.spec
        git commit -m "Update xremap to upstream version $version"
        git push
    fi
    sha=$(git rev-parse HEAD)

    gh release create "v$version" --repo "$repo" \
        --title "xremap $version" \
        --notes "Fedora RPM packages for xremap upstream version $version."

    echo "Waiting for the rpm workflow run for $sha to start..."
    run_id=""
    for _ in $(seq 1 30); do
        run_id=$(gh run list --repo "$repo" --workflow rpm.yml --event release \
            --json databaseId,headSha \
            --jq ".[] | select(.headSha == \"$sha\") | .databaseId" | head -n1)
        [ -n "$run_id" ] && break
        sleep 10
    done
    if [ -z "$run_id" ]; then
        echo "Error: no rpm workflow run appeared for v$version." >&2
        exit 1
    fi

    echo "Watching run $run_id for v$version..."
    gh run watch "$run_id" --repo "$repo" --exit-status --interval 30
    echo "v$version built and submitted to COPR."
done

echo
echo "Backfill complete."
