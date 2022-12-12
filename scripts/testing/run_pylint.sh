# To be run from the main folder.

docker run --rm -it -v "$PWD/src":"/code/src" dht22-monitor pylint ./src/