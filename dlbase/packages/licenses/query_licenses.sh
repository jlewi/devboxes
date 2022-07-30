#!/bin/bash -eu

# only used for changing license location in conda build
LICENSE_DIR="${1:-/usr/licenses}"
CHECK_LICENSE_DIR="${2:-${LICENSE_DIR}}"

declare -a UNLICENSED
function mark_unlicensed {
  UNLICENSED+=($1)
}

function download_license {
  local package=$1
  local output=$2
  local check_file=$3
  echo "checking license for ${package}."
  if [[ ! -f "${check_file}" ]]; then
    echo "searching license for: ${package}."
    set +e
    query_result=$(python ${BASH_SOURCE%/*}/query_license.py --name "${package}")
    query_code=$?
    # Get the last part of the returned string of query_license.py as the python
    # script might print multiple lines. However, the last part is always the
    # URL.
    query_result=$(echo "$query_result"|tr -s ""|rev|cut -f -1 -d" "|rev)
    set -e
    if [[ "${query_code}" -eq 0 ]]; then
      echo "package name: [${package}], package url: [${query_result}]"
      if ! $(wget --tries=10 -q "${query_result}" -O "${output}"); then
        mark_unlicensed "${package} - wrong link"
      fi
    elif [[ "${query_code}" -eq 1 ]]; then
      mark_unlicensed "${package} - ${query_result}"
    elif [[ "${query_code}" -eq 2 ]]; then
      echo "SKIPPED: ${query_result}"
    fi
  else
    echo "${check_file} already exists."
  fi
}

mkdir -p "${LICENSE_DIR}"
cd $(dirname $0)
IFS=$'\n'
for package in $(pip freeze); do
  if [[ $package =~ ^# ]] || [[ $package =~ ^-e ]]; then
    continue
  fi
  package_ref="${package%%==*}"

  # b/156206137
  # if the pip freeze result is any local file, ignore the local path and use the
  # package name as the reference.
  # example: "arrow @ file:///home/conda/feedstock_root/build_artifacts/arrow_1588902968139/work"
  PATTERN="\w+ @ file:/"
  if [[ $package_ref =~ $PATTERN ]]; then
    package_ref=$(echo $package_ref | cut -d" " -f 1)
  fi

  license_file="${LICENSE_DIR}/${package_ref}.LICENSE"
  check_license_file="${CHECK_LICENSE_DIR}/${package_ref}.LICENSE"
  download_license "${package_ref}" "${license_file}" "${check_license_file}"
done

readonly JUPYTER_LICENSE_DIR="${LICENSE_DIR}/jupyter"
readonly CHECK_JUPYTER_LICENSE_DIR="${CHECK_LICENSE_DIR}/jupyter"
mkdir -p "${JUPYTER_LICENSE_DIR}"
for package in $(jupyter labextension list 2>&1 | grep -E "enabled|disabled" | awk '{print $1}'); do
  package_ref="jupyter/${package}"
  license_file="${JUPYTER_LICENSE_DIR}/${package//\//_}.LICENSE"
  check_license_file="${CHECK_JUPYTER_LICENSE_DIR}/${package//\//_}.LICENSE"
  download_license "${package_ref}" "${license_file}" "${check_license_file}"
done

set +u  # workaround for 0-length array in older bash versions
if [[ "${#UNLICENSED[@]}" -ne 0 ]]; then
  echo "The following packages either are not approved or do not have licenses."
  printf "\t%s\n" "${UNLICENSED[@]}"
  exit 1
fi
set -u

echo "All licenses downloaded successfully."
