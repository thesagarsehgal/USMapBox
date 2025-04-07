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

FE View:
<img width="1435" alt="image" src="https://github.com/user-attachments/assets/cfabd019-f99a-43e1-8c02-a35c36834fc3" />


