#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

version_file="$SCRIPT_DIR/../sphinxcontrib/chapeldomain/__init__.py"
current_version=$(grep -E "VERSION\s*=\s*'[0-9.]+" "$version_file" | awk -F"=" '{print $2}' | tr -d ' ' | tr -d "'")
echo "Current version: $current_version"
major_version=$(echo "$current_version" | awk -F"." '{print $1}')
minor_version=$(echo "$current_version" | awk -F"." '{print $2}')
patch_version=$(echo "$current_version" | awk -F"." '{print $3}')


new_patch_version=$((patch_version + 1))
new_version="${major_version}.${minor_version}.${new_patch_version}"
echo "New version: $new_version"

# update the version file
set -x
sed -E "s|(VERSION[[:space:]]*=[[:space:]]*)'[^']+'|\1'${new_version}'|" "$version_file" > "${version_file}.tmp"
mv "${version_file}.tmp" "$version_file"
