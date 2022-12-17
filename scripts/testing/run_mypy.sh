# To be run from the main folder.

docker run --rm -it -v "$PWD":"/code/" room-monitor mypy --strict ./src/