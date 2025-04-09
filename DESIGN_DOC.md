# Design Document

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
   - Appropriate geometry sizing per boundary type. State boundaries geometry would be of simmilar sizes [less number of points] and counties boundaries would be more complex [more number of points] 
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

**Response:**
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

### Endpoint 3: Encompassing Areas
`GET /api/v1/encompassing?geo_id=<fips_code>`

**Response:**
```json
{
    "states": [
        {
            "name": "Utah",
            "fips_code": "49"
        }
    ],
    "counties": [
        {
            "name": "Morgan",
            "fips_code": "49029",
            "geometry": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [
                                        -111.26482,
                                        41.144253
                                    ],...
                                 ]
                              ]
                        }
                     }
                  ]
               }
         }
      ]
}
```

#### Geospatial Query Flow:

**Input:** System takes a geoid (like a FIPS code or boundary ID)

**Processing:**
- Looks up the polygon shape for that geoid
- Checks which states and counties fall inside that polygon using PostGIS's ST_Within()

**Output:**
Returns a clean list of:
- State IDs/names + their boundaries (as GeoJSON)
- County IDs/names + their boundaries (as GeoJSON)

**What Happens in UI:**
- Hover over a county chip → map highlights that county's border
- Mouse out → highlight disappears

**Why It's Fast:**
- Uses spatial indexes in PostGIS
- GeoJSON is lightweight for frontend rendering





**Further Additions that can be made :**
- Addition of smaller areas like Cities, ZipCodes
- Adding a Caching Layer for the GeoJSON data and the QuickFacts for frequently searched area  
