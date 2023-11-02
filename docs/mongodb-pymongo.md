# MongoDB and Pymongo Cheats


## Set up a MondoDB


Create a new Directory in your repository with a db folder in it. *Directory/db*

Create a YAML file named *docker-compose.yaml* and copy this script to it.


```
version: '3.6'
services:

  mongodb:
    image: mongo:3.6
    restart: unless-stopped
    volumes:
      - ./<Directory/db>:/data/db
    ports:
      - "27027:27017"
``` 


Run the commands below to create a docker container.


```
docker-compose up -d
docker run -d -p 27016:27017 --name mongo-client mongo:3.6
docker exec -it mongo-client bash
```

To get more information about the created container for example NAMES and PORTS run the *docker ps* command



## Database Manipulation in Python

The following code creates a databas with a variants collection.

```python
from pymongo import MongoClient
from datetime import datetime

db_client = MongoClient() # if you work on a vertual machine you might need to change this into db_client = MongoClient("<docker ps IP>",27017)
database = db_client["cnv_reference_db"]
var_coll = database["variants"]

variants = [
	{
	  "info": { "cn_count": 1 },
	  "biosample_id": "testsample-0001",
	  "variant_internal_id": '11:52900000-134452384:EFO_0030067',
	  "variant_state": { "id": 'EFO:0030067', "label": 'copy number loss' },
	  "location": {
	    "sequence_id": 'refseq:NC_000011.10',
	    "chromosome": '11',
	    "start": 52900000,
	    "end": 134452384
	  },
	  "relative_copy_class": 'partial loss',
	  "updated": datetime.now().isoformat()
	}
]

for v in variants:
	vid = var_coll.insert_one(v).inserted_id
	vstr = f'refvar-{vid}'
    var_coll.update_one({'_id':vid},{'$set':{ 'id':vstr }})
    print(f'==> inserted {vstr}')
```