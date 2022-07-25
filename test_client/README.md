##For building and testing in a local development environment the following steps can be used:

This is written from the perspective of using a Mac

Prerequisites:

docker
python


### Run the tests

- first start the dummy_pdf_or_png service by using the Makefile in the directory for the service
```
cd dummy-pdf-or-png
make run
```
   
- If all goes well you should now have that container running and you can test a request(use curl or httpie):
```http://localhost:3000/11```

Let the container run as some of the tests will need it

- Create and use new Pythen virtual env in test_client directory
```
cd ../test_client
python -m venv .venv
source .venv/bin/activate
```

- Install pipenv package and install required packages
```
pip install pipenv
pipenv install --dev
```

- Run the tests
```pytest```

Hopefully the tests will run successfully

### Build the test_client docker image and test it
```
docker build -t api-test:latest .
```

We now have a docker image called api-test

The image uses a required env variable called DUMMY_SERVICE_HOST So we start the image like this
```docker run --rm -p 8000:8000 -e DUMMY_SERVICE_HOST=host.docker.internal:3000 api-test:latest```

Because this service will need to be able to contact the dummy-pdf_or_png service running in docker DUMMY_SERVICE_HOST is set to host.docker.internal:3000

You should now be able to use httpie or curl (or browser) to acces the api on localhost:8000/{random number}

ex. ```http http://localhost:8000/11```

You will notice that we sometime gets a http code 204. That is when the upstream service returns an invalid pdf

### Running it on docker's kubernetes
Make sure to stop the container used for testing the test_client api or else the port 8000 will clash

You will need to have kuberneetes enabled in docker-desktop then make sure the kubectl context is set to docker-desktop by using this command
```kubectl config use-context docker-desktop```

You should now be able to use the deployment/service in the test_client.yaml by using this command
```kubectl create -f test_client.yaml```

and check for successful status with
```kubectl describe pods test-client```

on OSX to access the service we need to port-forward like this:
`kubectl port-forward test-client-xxxxxxxxxx-xxxxx 8000:8000` Where xxxxxxxx-xxxx can be tab-completed from the running pod
 
