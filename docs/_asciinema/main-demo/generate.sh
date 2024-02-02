#! /usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 2

rm -f output.cast
docker build -t your_image_name .

docker run -it \
    --rm \
    --sig-proxy \
    --name myimage \
    --hostname demo \
    -v ../../../:/salt-gnupg-rotate/:z \
    your_image_name \
    bash -c 'pip install --no-cache /salt-gnupg-rotate/; clear; asciinema-automation --asciinema-arguments " --overwrite --rows 24 --cols 120 --env SHELL,TERM,PATH -c \"env bash\"" /salt-gnupg-rotate/docs/_asciinema/main-demo/script.expect /salt-gnupg-rotate/docs/_asciinema/main-demo/output.cast'

    # bash -c 'pip install /salt-gnupg-rotate/; clear; asciinema-automation --delay 1 --standard-deviation 10 --wait 1000 --asciinema-arguments " --overwrite -c \"env -i bash\"" /salt-gnupg-rotate/docs/_asciinema/main-demo/script.sh /salt-gnupg-rotate/docs/_asciinema/main-demo/output.cast'
    # asciinema-automation

echo "Done recording! Playing back now."
asciinema play output.cast
# docker run -it --rm --name ubuntu -v ../../../:/salt-gnupg-rotate/:z ubuntu /salt-gnupg-rotate/docs/_asciinema/main-demo/script.sh
