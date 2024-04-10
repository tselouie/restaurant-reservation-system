# restaurant-reservation-system
Cloud-based Restaurant Reservation System: A scalable and user-friendly platform utilizing a microservices architecture with Python backend and ReactJS frontend.
Jira
https://lttse.atlassian.net/jira/software/projects/BTP405/boards/3/backlog
Github
https://github.com/tselouie/restaurant-reservation-system

docker build . -t reservation-api

Use this command to create the database:

```bash
docker run --name {ContainerName} -p 3306:3306 -e MYSQL_ROOT_PASSWORD={Password} -e MYSQL_DATABASE={DatabaseName} -d mysql:latest
```


Go to Google Cloud Run -> Artifact Registry -> New Repository
Install Gcloud CLI
```bash
gcloud init
gcloud auth login
gcloud auth configure-docker northamerica-northeast2-docker.pkg.dev

docker tag <local-tag> <repo-url>/<local-tag>
docker tag reservation-api:v3 northamerica-northeast2-docker.pkg.dev/eezcommerce/reservation-system/reservation-api:v3
docker push <repo-url> 
```

Cloud Run

Host