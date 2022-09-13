# APP platform

Run compute apps by letting users provide inputs as requested by the app.

## Usage

### Build the app docker

```sh
cd apps/tsp

docker build . -t app-tsp:dev
```

### Start Nocodb service

```sh
cd app_platform/

docker run -d --name nocodb \
-v $(pwd)/temp/:/data/ -p 8080:8080 \
nocodb/nocodb:latest
```

### Get the API token from nocodb service

Create any project in nocodb, click the project title name, and choose `copy auth token`.
Paste the auth token to `app_platform/settings.py`.

### Start the app platform

```sh
cd app_platform

python manage.py migrate

python manage.py runserver 8000
```

## Guide to run the TSP app

1. Create a project, and use `app-tsp:dev` as the `app_image` name.
2. Click `data` once the project is created, and create a few points in the `locations` table. For example

```
A | 1 | 2
B | 2 | 3
C | 4 | 0
```
3. Create a run by filling the `num_vehicles` and `depot_index` configs. You can use 1 and 0 respectively.
4. Click `save` to start the run.
5. Click on the `log` path of the run to see the results.