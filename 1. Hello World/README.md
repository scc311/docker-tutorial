# Hello World

`helloworld.sh` is a simple bash script that prints "Hello, world", asks for a name as input, then prints "Hello, |inputted name|"

`Dockerfile` can be used to build a simple Alpine Linux based container that will just contain the hello world script at `/app/helloworld.sh`. When run, this container will just run the script.

To Build:
```bash
docker build --rm -t 311tutorial:helloworld .
```

To Run:
```bash
docker run --rm -it -f Dockerfile 311tutorial:helloworld
```
