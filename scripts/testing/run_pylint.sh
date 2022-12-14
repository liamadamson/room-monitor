# To be run from the main folder.

docker run --rm -it -v "$PWD/src":"/code/src" -v "$PWD/.pylintrc":"/code/.pylintrc" room-monitor pylint ./src/