#!/bin/bash

BASE_DIR="$(dirname $0)"
REPO_PATH="${BASE_DIR}/.."
IMAGE="${1}"
VERSION="${2}"
ARCH="${3}"

tag_and_push() {
  [[ $ARCH == "x86" ]] && docker tag "comworkio/${2}:latest" "comworkio/${2}:${1}"
  docker tag "comworkio/${2}:latest-${ARCH}" "comworkio/${2}:${1}-${ARCH}"
  docker push "comworkio/${2}:${1}"
}

cd "${REPO_PATH}" && git pull origin master || : 
sha="$(git rev-parse --short HEAD)"
echo '{"version":"'"${VERSION}"'", "sha":"'"${sha}"'", "arch":"'"${ARCH}"'"}' > manifest.json

COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker-compose-build-${ARCH}.yml build --no-cache "${IMAGE}"

echo "${DOCKER_ACCESS_TOKEN}" | docker login --username comworkio --password-stdin

[[ $ARCH == "x86" ]] && docker-compose push "${IMAGE}"
tag_and_push "${VERSION}" "${IMAGE}"
tag_and_push "${VERSION}-${CI_COMMIT_SHORT_SHA}" "${IMAGE}"

git add .
git stash
git stash clear
