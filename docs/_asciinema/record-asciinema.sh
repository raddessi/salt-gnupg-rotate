#! /usr/bin/env bash

function show_help() {
    echo "Usage: ${0} <asciinema-automation expect script>"
    echo
    echo "You will need docker or podman along with the agg application from:"
    echo "    https://github.com/asciinema/agg"
    echo
    echo "Options:"
    echo "    -h, --help    Display this help message and exit."
    echo "    -f, --file    Path to the expect script to run."
    echo "    --no-rebuild  Skip the rebuild the docker image before running"
}

# Check if no arguments were passed
if [ $# -eq 0 ]; then
    echo "No arguments provided."
    show_help
    exit 1
fi

# Defaults
DOCKER_IMAGE=salt-gnupg-rotate-asciinema
GIT_TOP_DIRPATH=$(git rev-parse --show-toplevel)
REBUILD=true

# Loop through all arguments
while [[ ${#} -gt 0 ]]; do
    if [ -z "${2}" ]; then
        echo "No argument passed for keyword $1"
        exit 2
    fi
    case $1 in
    -h | --help)
        show_help
        exit 0
        ;;
    -f | --file)
        FPATH="$(realpath $2)"
        if ! [ -f "${FPATH}" ]; then
            echo "No such file ${FPATH}"
            exit 4
        fi
        shift
        ;;
    --no-rebuild)
        REBUILD=false
        ;;
    *)
        # Handle other arguments
        echo "Unknown keyword: $1" >&2
        exit 3
        ;;
    esac
    shift
done

# we will eventually write the output cast to the same directory as the expect script,
# with the same name
OUTPUT_DIRPATH=$(dirname "$(realpath ${FPATH})")
CAST_FNAME=$(basename "${FPATH%.expect}".cast)
GIF_FNAME=$(basename "${FPATH%.expect}".gif)

# change working dir to the top level of the git repo
cd "${GIT_TOP_DIRPATH}" || exit 2

echo -e "Cleaning up previous recording casts ..."
rm -f "${OUTPUT_DIRPATH}/${CAST_FNAME}"

if [ ${REBUILD} == "true" ]; then
    echo -e "\nBuilding docker image ..."
    docker build -t ${DOCKER_IMAGE} -f ./Dockerfile.asciinema .
fi

echo -e "\nRunning asciinema-automation in docker ..."
docker run \
    -it \
    --rm \
    --sig-proxy \
    --name myimage \
    --hostname demo \
    -v "${OUTPUT_DIRPATH}:/output/:z" \
    ${DOCKER_IMAGE} \
    bash -c " \
        asciinema-automation \
            --delay 5 \
            --standard-deviation 15 \
            --asciinema-arguments ' \
                --overwrite \
                --rows 24 \
                --cols 120 \
                --env SHELL,TERM,PATH \
                -c \"env bash\" \
            ' \
            '$(realpath --relative-to=${GIT_TOP_DIRPATH} ${FPATH})' \
            '/output/${CAST_FNAME}' \
    "

echo -e "\nDone recording! Cast saved to ${OUTPUT_DIRPATH}/${CAST_FNAME}"
echo "Converting to gif ${OUTPUT_DIRPATH}/${GIF_FNAME} ..."
agg \
    --theme monokai \
    --font-size 20 \
    --speed 1 \
    --rows 24 \
    --cols 120 \
    "${OUTPUT_DIRPATH}/${CAST_FNAME}" \
    "${OUTPUT_DIRPATH}/${GIF_FNAME}"

echo -e "\nPlaying back the cast now:"
asciinema play "${OUTPUT_DIRPATH}/${CAST_FNAME}"
