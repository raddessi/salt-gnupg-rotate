#! /usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 2

rm -f output.cast
docker build -t your_image_name -f ../../../Dockerfile.asciinema ../../../

docker run -it \
    --rm \
    --sig-proxy \
    --name myimage \
    --hostname demo \
    -v .:/output/:z \
    your_image_name \
    bash -c 'asciinema-automation --delay 5 --standard-deviation 15 --asciinema-arguments " --overwrite --rows 24 --cols 120 --env SHELL,TERM,PATH -c \"env bash\"" /salt-gnupg-rotate/docs/_asciinema/main-demo/script.expect /output/output.cast'

echo "Done recording! Playing back now."
asciinema play output.cast
