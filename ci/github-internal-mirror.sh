#!/bin/bash

SRC_PATH="/home/centos/cmd-api/"
TARGET_PATH="/home/centos/cmd-api-internal/"

cd "${TARGET_PATH}" && git pull origin master || :
cd "${SRC_PATH}" && git pull origin master || :

files_to_excule=("LICENCE" ".gitlab-ci.yml" "Dockerfile.arm" "deployment.yaml" "docker-compose-build-arm.yml")

for i in *; do
  if [[ $i != "ci" ]] && [[ -d "${i}" ]]; then
    rm -rf "${TARGET_PATH}/${i}"
    cp -R "${i}" "${TARGET_PATH}"
  fi

  if [[ -f "${i}" ]]; then
    rm -rf "${TARGET_PATH}/${i}"
    cp "${i}" "${TARGET_PATH}"
  fi
done

for i in "${files_to_excule[@]}"; do
  rm -rf "${TARGET_PATH}/${i}"
done

commit_msg=$(git log -1 --pretty=%B|sed '$ d')
[[ $commit_msg ]] || commit_msg="Automatic update"

cd "${TARGET_PATH}" && git pull origin master || :
sed -i "7,18d;25,40d;s/\ (even a raspberrypi)//g" README.md

git add .
git commit -m "${commit_msg}"
git push origin master 

exit 0
