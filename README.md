# PredictingFlightDelays


# Instructions and Setup Guide

## Containerize the application using Docker

1. Build the Docker Image
  
```bash
$ docker build  -t fastapi-ml .
```

2. Start the container:

```bash
$ docker run -p 80:80 fastapi-ml
```

3. Test the Docker container with an example request:

- Option 1: Using the web browser. 

  Visit `http://0.0.0.0:8000/docs`. You will see a /predict endpoint: 


You can click on "Try it now" which will let you modify the input request. Click on "Execute" to see the model prediction response from the web server.


  - Option 2: Using the command line:

```bash
$ curl -X 'POST' \
'http://0.0.0.0/predict' \
-H 'Content-Type: application/json' \
-d '{
    "DepartureDateTime": "12/12/2022 15:15:15",
    "Origin":"JFK",
    "Destination":"ATL"
    }'
```

## Local testing & examining logs

1. Find out the container id of the running container:
```bash
$ docker ps
```

This will return a response like the following:
```bash

CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS         PORTS                NAMES
f9b59902e94f   fastapi-ml   "uvicorn main:app --…"   10 minutes ago   Up 10 minutes   0.0.0.0:80->80/tcp   brave_liskov
```

2. SSH into the container using the container id from above: 

```bash
$ docker exec -it <container id> /bin/sh
```

3. Tail the logs:
```bash
$ tail -f ../data/logs.out
```

4. Now when you send any request to the web server (from the browser, or another tab in the command line), you can see the log output coming through in `logs`. Test the web server with these requests and make sure you can see the outputs in `logs`:



```bash
{
    "DepartureDateTime": "24/12/2023 19:15:00",
    "Origin":"JFK",
    "Destination":"ATL"
}
```
```bash
{
    "DepartureDateTime": "01/01/2023 15:15:00",
    "Origin":"DTW",
    "Destination":"JFK"
}
```
```bash
{
    "DepartureDateTime": "04/07/2022 09:15:00",
    "Origin":"SEA",
    "Destination":"ATL"
}
```
```bash
{
    "DepartureDateTime": "12/12/2022 22:30:00",
    "Origin":"DTW",
    "Destination":"MSP"
}
```
