### Running the application 

1. Running the docker compose container 
```
docker-compose up --build
```

2. run the script to load the downloaded script into the databse  

2.1 Enter into the docker container of the backend service   
```
docker-compose exec tsgbe sh
```
2.2. Run commands to load the scrapped data in the database
```
cd src/scripts 
python load_db.py
```

Prereq: To run the scrapper, to extract all the data from the website, run the following command `python load_db.py`, whcih loads data in `src/scripts/csv_files`

3. access the FE from localhost:3000, BE from localhost:8080/docs and DB from localhost:5433/census_db  


