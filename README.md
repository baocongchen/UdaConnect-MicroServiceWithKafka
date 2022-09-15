# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### Technologies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster

## Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
4. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
5. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`.
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Steps
Do `vagrant ssh` to login to your vagrant virtual machine, clone the repository, change directory `cd UdaConnect-MicroServiceApp`, then perform the following steps
1. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
2. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
3. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS
4. `kubectl apply -f deployment/udaconnect-person-api.yaml` - Set up the service and deployment for the Person API
4. `kubectl apply -f deployment/udaconnect-location-api.yaml` - Set up the service and deployment for the Location API
4. `kubectl apply -f deployment/udaconnect-connection-api.yaml` - Set up the service and deployment for the Connection API
5. `kubectl apply -f deployment/udaconnect-frontend-app.yaml` - Set up the service and deployment for the web app
6. `kubectl apply -f deployment/kafka.yaml` - Set up the service and deployment for kafka server
7. Follow [the instruction](https://docs.bitnami.com/tutorials/deploy-scalable-kafka-zookeeper-cluster-kubernetes) to create a kafka topic called `location` 
8. `sh scripts/run_db_command.sh <POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`)
9. `kubectl apply -f deployment/udaconnect-location-producer.yaml` - Set up the service and deployment for gRPC Producer
10. `kubectl apply -f deployment/udaconnect-location-consumer.yaml` - Set up the deployment for gRPC Consumer

Manually applying each of the individual `yaml` files is cumbersome but going through each step provides some context on the content of the starter project. In practice, we would have reduced the number of steps by running the command against a directory to apply of the contents: `kubectl apply -f deployment/`.

Note: The first time you run this project, you will need to seed the database with dummy data. Use the command `sh scripts/run_db_command.sh <POD_NAME>` against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`). Subsequent runs of `kubectl apply` for making changes to deployments or services shouldn't require you to seed the database again!

### Verifying it Works
Once the project is up and running, you should be able to see all the deployments and services in Kubernetes:

```
NAME                                        READY   STATUS    RESTARTS       AGE
postgres-554d66564b-2bwkx                   1/1     Running   0              21h
udaconnect-connection-api-fdb6567d9-jg52p   1/1     Running   0              21h
udaconnect-frontend-app-84bff8d64-2mx2n     1/1     Running   0              21h
udaconnect-location-api-cf8f7bf84-vtvxd     1/1     Running   0              21h
kafka-zookeeper-0                           1/1     Running   0              21h
udaconnect-person-api-7bb457d84d-qnl7v      1/1     Running   0              21h
kafka-0                                     1/1     Running   0              21h
location-producer-6689567fd5-jjgrb          1/1     Running   0              10m
location-consumer-5769fdb566-8dp67          1/1     Running   1 (2m1s ago)   10m
```

```
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kubernetes                  ClusterIP   10.43.0.1       <none>        443/TCP                      46h
kafka-zookeeper-headless    ClusterIP   None            <none>        2181/TCP,2888/TCP,3888/TCP   21h
kafka-zookeeper             ClusterIP   10.43.214.114   <none>        2181/TCP,2888/TCP,3888/TCP   21h
kafka-headless              ClusterIP   None            <none>        9092/TCP,9093/TCP            21h
kafka                       ClusterIP   10.43.239.16    <none>        9092/TCP                     21h
postgres                    NodePort    10.43.102.194   <none>        5432:32128/TCP               21h
udaconnect-connection-api   NodePort    10.43.205.35    <none>        5003:30003/TCP               21h
udaconnect-frontend-app     NodePort    10.43.166.46    <none>        3000:30000/TCP               21h
udaconnect-location-api     NodePort    10.43.232.109   <none>        5001:30001/TCP               21h
udaconnect-person-api       NodePort    10.43.1.193     <none>        5002:30002/TCP               21h
location-producer           NodePort    10.43.69.167    <none>        5005:30005/TCP               12m
```

These pages should also load on your web browser:
* `http://localhost:30001/` - OpenAPI Documentation for Location API
* `http://localhost:30001/api/locations` - Base path for Location API
* `http://localhost:30002/` - OpenAPI Documentation for Person API
* `http://localhost:30002/api/persons` - Base path for Person API
* `http://localhost:30003/` - OpenAPI Documentation for Connection API
* `http://localhost:30003/api//persons/<person_id>/connection` - Base path for Connection API
* `http://localhost:30000/` - Frontend ReactJS Application

#### Deployment Note
You may notice the odd port numbers being served to `localhost`. [By default, Kubernetes services are only exposed to one another in an internal network](https://kubernetes.io/docs/concepts/services-networking/service/). This means that `udaconnect-frontend-app`, `udaconnect-person-api`, `udaconnect-location-api`, and `udaconnection-connection-api` can talk to one another. For us to connect to the cluster as an "outsider", we need to a way to expose these services to `localhost`.

Connections to the Kubernetes services have been set up through a [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). (While we would use a technology like an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) to expose our Kubernetes services in deployment, a NodePort will suffice for development.)

### Docker Images
`udaconnect-frontend-app`, `udaconnect-person-api`, `udaconnect-location-api`, and `udaconnection-connection-api` use docker images hosted on [docker hub](https://hub.docker.com/u/petetran). 

## Configs and Secrets
In `deployment/db-secret.yaml`, the secret variable is `d293aW1zb3NlY3VyZQ==`. The value is simply encoded and not encrypted -- this is ***not*** secure! Anyone can decode it to see what it is.
```bash
# Decodes the value into plaintext
echo "d293aW1zb3NlY3VyZQ==" | base64 -d

# Encodes the value to base64 encoding. K8s expects your secrets passed in with base64
echo "hotdogsfordinner" | base64
```
This is okay for development against an exclusively local environment and we want to keep the setup simple so that you can focus on the project tasks. However, in practice we should not commit our code with secret values into our repository. A CI/CD pipeline can help prevent that.

## PostgreSQL Database
The database uses a plug-in named PostGIS that supports geographic queries. It introduces `GEOMETRY` types and functions that we leverage to calculate distance between `ST_POINT`'s which represent latitude and longitude.

_You may find it helpful to be able to connect to the database_. In general, most of the database complexity is abstracted from you. The Docker container in the starter should be configured with PostGIS. Seed scripts are provided to set up the database table and some rows.
### Database Connection
While the Kubernetes service for `postgres` is running (you can use `kubectl get services` to check), you can expose the service to connect locally:
```bash
kubectl port-forward svc/postgres 5432:5432
```
This will enable you to connect to the database at `localhost`. You should then be able to connect to `postgresql://localhost:5432/geoconnections`. This is assuming you use the built-in values in the deployment config map.
### Software
To manually connect to the database, you will need software compatible with PostgreSQL.
* CLI users will find [psql](http://postgresguide.com/utilities/psql.html) to be the industry standard.
* GUI users will find [pgAdmin](https://www.pgadmin.org/) to be a popular open-source solution.

## Architecture Diagrams
Refer to [Lucidchart](./docs/architecture_design.png)

