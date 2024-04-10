# restaurant-reservation-system
Cloud-based Restaurant Reservation System: A scalable and user-friendly platform utilizing a microservices architecture with Python backend and ReactJS frontend.
Jira
https://lttse.atlassian.net/jira/software/projects/BTP405/boards/3/backlog
Github
https://github.com/tselouie/restaurant-reservation-system

docker build . -t reservation-api

Go to Google Cloud Run -> Artifact Registry -> New Repository
Install Gcloud CLI
```bash
gcloud init
gcloud auth login
gcloud auth configure-docker northamerica-northeast2-docker.pkg.dev

docker tag <local-tag> <repo-url>/<local-tag>
docker tag reservation-api northamerica-northeast2-docker.pkg.dev/eezcommerce/reservation-system/reservation-api:latest
docker push <repo-url> 
```

Cloud Run

Host