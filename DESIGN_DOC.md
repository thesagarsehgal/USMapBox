# Geospatial Analytics System Design Document

## Data Acquisition Process

### Census Data Extraction
1. **Primary Data Source**: 
   - US Census QuickFacts API (CSV format)
   - Endpoint: `https://www.census.gov/quickfacts/fact/csv/US`

2. **Geographic Lookup API**:
   - Search endpoint: `https://www.census.gov/quickfacts/search/json/?type=geo&search=Alaska`
   - Returns: `geo_id`, area codes, and metadata

3. **Boundary Data**:
   - Source: Converted GeoJSON files from [Eric Clst's Portal](https://eric.clst.org/tech/usgeojson/)
   - Original Source: [US Census Cartographic Boundary Files](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)

## Database Schema

### Tables Structure

#### `states`
| Column        | Type         | Description               |
|---------------|--------------|---------------------------|
| state_fips    | VARCHAR(2)   | Primary Key (e.g. '04')   |
| state_name    | VARCHAR(100) | Official state name       |
| census_area   | FLOAT        | Total area in sq. miles   |
| geometry      | GEOMETRY     | PostGIS spatial data      |

#### `counties`
| Column        | Type         | Description                     |
|---------------|--------------|---------------------------------|
| county_fips   | VARCHAR(5)   | Primary Key (e.g. '04013')      |
| county_name   | VARCHAR(100) | Official county name            |
| state_fips    | VARCHAR(2)   | Foreign Key to states table     |
| census_area   | FLOAT        | Total area in sq. miles         |
| geometry      | GEOMETRY     | PostGIS spatial data            |

#### `quickfacts`
| Column        | Type         | Description                     |
|---------------|--------------|---------------------------------|
| fips_code     | VARCHAR(5)   | Composite Primary Key (Part 1)  |
| fact_name     | VARCHAR(255) | Composite Primary Key (Part 2)  |
| fact_value    | TEXT         | Demographic/metric value        |
| location_type | VARCHAR(10)  | 'state' or 'county'             |

## Architectural Decisions

### Database Design Rationale
1. **Separate Boundary Tables**:
   - Better spatial indexing performance
   - Simplified query patterns
   - Appropriate geometry sizing per boundary type
   - Alternative: A single table with `parent_fips` would require complex spatial queries
   - Also, the hierarchy of this is limited so, separate tables could be maintained

2. **Fact Storage Approach**:
   - Flexible EAV (Entity-Attribute-Value) model for demographic facts
   - Idempotent data loading (updates existing records without duplication)

## API Specification

### Endpoint 1: Boundary Data
`GET /api/v1/boundaries?boundary_type=<state|county>`

**Response (GeoJSON):**
```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": "04",
                "name": "Arizona"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": []
            }
        }
    ]
}
```

### Endpoint 2: Demographic Data
`GET /api/v1/data?geo_id=<fips_code>`

**Response (GeoJSON):**
```json
{
    "location_id": "02",
    "location_name": "Alaska",
    "facts": [
        {
            "fact_name": "Population density",
            "fact_value": "1.2"
        },
        {
            "fact_name": "Total population",
            "fact_value": "740,133"
        }
    ]
}
```

Furhter Additions:
- Additoon of smaller areas like Cities, ZipCodes
- Proximity Search 
- Adding Caching Layer for the GeoJSON data and the QuickFacts for freuqntky searched area  
