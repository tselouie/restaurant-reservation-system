# Restaurant Reservation System
Cloud-based Restaurant Reservation System: A scalable and user-friendly platform utilizing a microservices architecture with Python backend and ReactJS frontend.
The front end and back end portions of this project are split into the subdirectories: front & backend.


[Github Repository Link](https://github.com/tselouie/restaurant-reservation-system/)

### Directory backend Structure

| File          | Description                                           |
|---------------|-------------------------------------------------------|
| Dockerfile    | Defines the Docker image for the server.              |
| server.py     | Contains the implementation of the HTTP server.       |
| .env.example  | Defines the structure for a .env file.                |
| db            | Contains 4 files that defines the interactions w/ database.    |
| handlers      | Defines how requests are handled and contains a separate handler for each table.    |
| test          | Contains a unit test for each of the tables.    |

# Run Locally

Navigate to the folder ~/backend

# API Testing

If you want to test the http handlers you can go to backend/tests and run any of the following tests in the backend/tests directory:
```bash
python test_db_customers.py
python test_db_reservations.py
python test_db_tables.py
```

Use this command to create a network
```bash
docker network create {NetworkName}
```

Use this command to create the database:

```bash
docker run --name {ContainerName} -p 3306:3306 -e MYSQL_ROOT_PASSWORD={Password} -e MYSQL_DATABASE={DatabaseName} -d mysql:latest
```
Remember the ContainerName,Password, and DatabaseName as we will use them for our environment variables.

Create `.env` file and use the values we used to create the database
```bash
DATABASE_URL=localhost
DATABASE_PASSWORD={Password}
DATABASE_NAME={DatabaseName}
DATABASE_USER=root
```
Install dependencies for the code

```bash
pip install python-dotenv mysql-connector-python
or
python -m pip install python-dotenv mysql-connector-python
```

Run the server - 
*On first run, the server will create the tables.*
```bash
python server.py
```

#### Containerize using Docker

Create Docker files:
```bash 
touch Dockerfile
```
Build our app using the settings in Dockerfile
```bash
docker build -t reservation-system:version .
```
Once the image is built, you can run the Docker container using the following command:
```bash
docker run -dp 8010:8010 reservation-system
```

Now we have an image of our Restful API and a local mySQL database container running.
We can launch now launch our frontend! Do this by going to the frontend directory.
`cd front`

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.


# Deploy Services to the Cloud

## Deploy to Rest API to GCloud
Go to Google Cloud Console -> Artifact Registry -> New Repository

Once you have created a resository in the Artifact Registry you can setup your image to be pushed to google.
[Install Gcloud CLI](https://cloud.google.com/sdk/docs/install)
Run these commands:
```bash
## Setup
gcloud init
gcloud auth login
### <zone> can be obtained from the Artifact Registry inside your GCloud Console
gcloud auth configure-docker <zone> northamerica-northeast2-docker.pkg.dev
docker tag <local-tag> <repo-url>/<local-tag>
docker push <repo-url> 
#e.g.
docker tag reservation-api:v1 northamerica-northeast2-docker.pkg.dev/eezcommerce/reservation-system/reservation-api:v1
docker push northamerica-northeast2-docker.pkg.dev/eezcommerce/reservation-system/reservation-api:v1
```

Now if your push to google was successful you can go back to cloud.google.com console and navigate to Cloud Run and create service
*!!!Note you may be charged for creating this service*

All the settings and images will be requested when you create the service. Once it is successfully run a URL will be provided which you can use to access from your ReactJS interface.


### Front End Directory

| File          | Description                                           |
|---------------|-------------------------------------------------------|
| index.js      | Application entrypoint.                               |
| App.js        | The initial component that is rendered.               |
| server.py     | Contains the implementation of the HTTP server.       |
| .env.example  | Defines the structure for a .env file in the react app. |
| dashboard     | Contains all the components that the application renders |
| public      | assets that are accessible externally                   |
| lib          | Contains a utility to shorten the classnames used by tailwind. |

## Deploy ReactJS front end to Github-Pages
[Link to gh-pages Documentation](https://github.com/gitname/react-gh-pages)
Nothing really to say here, just follow the instructions and github will provide you a URL to the front-end website, just be certain to update your routes with a base url.


