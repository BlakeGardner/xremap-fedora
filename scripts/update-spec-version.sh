#!/usr/bin/env bash
# Update xremap.spec to package a new upstream version:
#   1. Sets Version to the given version.
#   2. Resets Release to 1%{?dist}.
#   3. Prepends a %changelog entry for the new version.
#
# Usage: ./scripts/update-spec-version.sh <version>

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>" >&2
    exit 1
fi

version="$1"
if ! [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: '$version' does not look like an upstream version (X.Y.Z)." >&2
    exit 1
fi

spec="$(dirname "$0")/../xremap.spec"

sed -i "s/^Version:.*/Version:        $version/" "$spec"
sed -i "s/^Release:.*/Release:        1%{?dist}/" "$spec"

entry="* $(LC_ALL=C date +'%a %b %d %Y') Blake Gardner <blakerg@gmail.com> - $version-1
- Update xremap to upstream version $version
"
awk -v entry="$entry" '{ print } $0 == "%changelog" { print entry }' "$spec" > "$spec.tmp"
mv "$spec.tmp" "$spec"

echo "xremap.spec updated to version $version."
