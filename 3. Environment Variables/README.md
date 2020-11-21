# Environment Variables


## Part 1: Building the image

This container will run a simple Python webserver built on the flask framework. This uses the image from Docker Hub `python:3-alpine3.10`.

```bash
docker build --rm -t 311tutorial:envvars .
```

## Part 2: Changing the variable

This webserver will display the value of the env var `MYVAR`.
An envvar is not attached to a specific programing language. Many languages have a way to get and set them. In this case, it is Python, but Java, JS, Golang etc... all have his ability. The container built has an env var `MYVAR` that is set to the string `default` as defined in the Dockerfile. This can be changed when creating an instance of the container (when running it) with the `-e` flag. Like so:
```bash
docker run --rm -it -p 42069:80 -e MYVAR="docker is great" 311tutorial:envvars
```

Now, go to `http://localhost:42069` on your web browser to see the webpage!

> Try setting MYVAR to something else too, remember, you don't have to rebuild the container, only rerun!
