# JAVA RMI

This uses the calculator example for RMI that can be found on moodle [here](https://modules.lancaster.ac.uk/mod/page/view.php?id=1416434). 

The code can be found here in `original` directory. A solution to this task can be found in the `solution` directory.

Below is an example architecture of 2 rmi clients in separate docker containers and a server container that also runs an rmi registry:
```ascii
   ---------------------------------------------------------------- rmicw network
         |             |                 |
         |             |                 |port 1099
         |             |                 |
       +----------+  +----------+      +---------------+
       |rmi       |  |rmi       |      |rmi server     |
       |client 1  |  |client 2  |      |and registry   |
       +----------+  +----------+      +---------------+
    +-----------------------------------------------------+
    |                                                     |
    |                       docker                        |
    +-----------------------------------------------------+
```
The `rmicw` is a network that lets all containers communicate. It is good practice to have separate networks for services to communicate over. To create the network, run:
```bash
docker network create rmicw
```

## Lets Begin

Firstly, separate the code into 3 catagories:
 - Code **only** the client needs
   - into a folder called `client-code`
 - Code **only** the server needs
   - into a folder called `server-code`
 - Code **both** the client and server need (like interfaces)
   - into a folder called `shared-code`

## Dockerfile for the Client

In the `client-code` directory, make a new file called `Dockerfile`. For the client, we can start off with alpine linux as it is a nice small base image. We will also need to install a JDK such as `openjdk8`. This looks like so:
```Dockerfile
FROM alpine:latest
RUN apk add --no-cache openjdk8
ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"
```
Here the Java is also "installed" (added to the PATH).

Next, the files for both the shared code and client code need to be copied into the same folder in the container.
```Dockerfile
WORKDIR /app
COPY client-code/ .
COPY shared-code/ .
```
Now both sets of code are in the `/app` directory in the container image.

Finally, we need to compile the code and tell the container to run the code when instantiated!
```Dockerfile
RUN javac *.java
ENTRYPOINT [ "java", "calculatorclient" ]
```

Now the docker container for a client can be created. This should be run from the projects root directory (where you can see the separated folders created in the lets begin step):
```bash
docker build --rm -f client-code/Dockerfile -t 311tutorial:rmi-client .
```

Using `-f` here tells docker to use the dockerfile from the client code directory as it typically defaults to `./Dockerfile`.

## Dockerfile for the Server

In the `server-code` directory, make a new `Dockerfile`. Much like for the client, it can start off with alpine with a Java install.
```Dockerfile
FROM alpine:latest
RUN apk add --no-cache openjdk8
ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"
```

Next, the files for both the shared code and server code need to be copied into the same folder in the container.
```Dockerfile
WORKDIR /app
COPY server-code/ .
COPY shared-code/ .
```
Now both sets of code are in the `/app` directory in the container image.

To be able to run both the registry and the code when the container starts, a simple bash script can be created like so:
```bash
#!/bin/bash

rmiregistry &
java calculatorserver
```
Call this file `entrypoint.sh` and put it in the `server-code` folder, and make it executable in the container:
```Dockerfile
RUN chmod +x entrypoint.sh
```

Finally, we need to compile the code and tell the container to run the entrypoint script at the start:
```Dockerfile
RUN javac *.java
ENTRYPOINT [ "sh", "entrypoint.sh" ]
```

Now the docker container for a server can be created. This should be run from the projects root directory (where you can see the separated folders created in the lets begin step):
```bash
docker build --rm -f server-code/Dockerfile -t 311tutorial:rmi-server .
```

## Running your server and registry

- Using the `--network` flag, we can attach a container to a network
- using the `--name` flag, a hostname for the container can be set
```bash
docker run --rm --network rmicw --name rmiserver 311tutorial:rmi-server
```

## Running your client

From another terminal window...<br>
Using the `--network rmicw` flag, we can attach a container to a network:
```bash
docker run --rm --network rmicw 311tutorial:rmi-client
```

## Oh No

The client is performing a registry lookup on `localhost`, but the registry is no longer at `localhost`! As the `--name` flag gave the server container the hostname `rmiserver`, the naming lookup must be performed there, so replacing `localhost` with `rmiserver` should fix that (in `calculatorclient.java` line `22`).

You could have the host name set via a environment variable though, right...?

This code might help with that:
```java
import java.util.stream.*;
import java.nio.file.*;
import java.io.*;

public class dockerutility {

  public static String getRegistryHost() {

    boolean isDocker = false;

    try (Stream < String > stream =
      Files.lines(Paths.get("/proc/1/cgroup"))) {
      isDocker = stream.anyMatch(line -> line.contains("/docker"));
    } catch (IOException e) {
      System.out.println("Not running in Docker 😢");
    }
    if (isDocker) {
      System.out.println("Running in Docker! 🐳");
      if (System.getenv("REGISTRY_HOST") != null)
        return System.getenv("REGISTRY_HOST");
      System.out.println("🐳⚠️  Please set the REGISTRY_HOST environment variable!");
    }
    return "localhost";
  }

}
```
The just run the client like so:
```bash
docker run --rm --network rmicw -e REGISTRY_HOST=|registry-container-hostname| 311tutorial:rmi-client
```
