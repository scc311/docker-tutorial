# Minecraft Server

This covers: 
 - Using Build Arguments
 - Making more complex Dockerfiles
 - Mounting Volumes for storage purposes
 - Running multiple versions at the same time
 - Using tags properly

In this folder is a Dockerfile that uses Alpine Linux. It also installs the Java 8 runtime environment (installed using the Alpine's package manager `apk`). It copies in the default server settings found in the `defaults` directory and downloads a Minecraft server jar file corresponding to the version in the **build argument** `SERVER_VERSION`.

A build argument is only usable within the build time. Once the container is built, it is not usable. This is how it differs to an environemnt variable. It is set in the file and can be overwritten in the `docker build` command with the `--build-arg` flag. unlike the environment variable that was set in the `docker run` command.

To build the container with the default `SEVER_VERSION` value (the value defined in the Dockerfile), just run:
```bash
docker build --rm -t 311tutorial:mc1.16 .
```

To build with another version, for example 1.15.2, run:
```bash
docker build --rm -t 311tutorial:mc1.15 --build-arg SERVER_VERSION=1.15.2 .
```
> You should tag you image with the version somewhere after the `:` like in the command above

## Running the Server

The default port Minecraft uses is port `25565`, so when running we should map that. We can use `42069` again if the web server container is stopped!

```bash
docker run --rm -it -p 42069:25565 311tutorial:mc1.16
```
> Use the tag from the steps above, this will run version 1.16.4

## Saving the World

You minecraft world is generated in the container's file system, thus when the container stops and is removed, the world will be deleted! To save your world, you can use volume mounting like so:
```bash
docker run --rm -it -p 42069:25565 -v $PWD/world:/server/world 311tutorial:mc1.16
```