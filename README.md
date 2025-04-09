# Running the Application

### 1. Start Docker Containers
Use the following command to build and run the Docker containers:

```
docker-compose up --build
```

### 2. Load Data into the Database
After the containers are running:

#### 2.1. Enter the backend service container:
```
docker-compose exec tsgbe sh
```

#### 2.2. Run the data loading script:
```
cd src/scripts
python load_db.py
```
Note: The load_db.py script loads data into the database from CSV files located in src/scripts/csv_files.

### 3. Accessing the Services
Frontend: http://localhost:3000
Backend (Swagger Docs): http://localhost:8080/docs
PostgreSQL DB: localhost:5433, database name: census_db

### Optional: Run the Scraper Separately
To scrape and generate data (if not already downloaded), you can directly run:

```
python src/scripts/load_db.py
```

### [Loom Demo Video](https://www.loom.com/share/dcffe1494bd64209a5507566a0180ded?sid=838a85d6-4ae6-4c5f-85c8-e8fa685cc1df)


### FE View:
<img width="1434" alt="image" src="https://github.com/user-attachments/assets/90a20871-0ac7-4eaf-8c06-70558d09816a" />
<img width="1440" alt="Screenshot 2025-04-09 at 4 38 40 PM" src="https://github.com/user-attachments/assets/1b83d72b-539f-4eb7-8332-666c4c736e3f" />

