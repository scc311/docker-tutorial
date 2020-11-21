# Web Server


## Part 1: Building the image (based on NGINX)

To build the image that will copy in the HTML files, simply run:
```bash
docker build --rm -t 311tutorial:webserver .
```

## Part 2: Running the web server

The web server will run inside the container on port `80` by default. However, to show how port mapping works, we want to be able to access the webserver on port `42069`. To map port 80 of the container to your machine's port 42069, add the flag `-p 42069:80` to the docker run command:
```bash
docker run --rm -it -p 42069:80 311tutorial:webserver
```

Now, go to `http://localhost:42069` on your web browser to see the webpage!

> Try moving the port mapping to another port (such as 8080) `-p 8080:80`

You will notice, that if you change the contents of `index.html` whilst the container is running, it will not change on the website when you refresh. This is because the container has its own copy. To get the new content, you must close, rebuild, and then rerun the container. This can be annoying when developing.

## Part 3: Volume Mounts

To make the container use our filesystem's copy of `index.html`, we can use volume mounting.

For this, we will use the nginx image from Docker Hub `nginx:alpine`. This webserver shows the contents of `/usr/share/nginx/html`.

So, to mount this, run:
```bash
docker run --rm -it -p 42069:80 -v $PWD/html:/usr/share/nginx/html nginx:alpine
```
Now changes to the `index.html` file should be present when refreshing the webpage, without rebuilding and rerunning the container!
