# MongoDB and Pymongo Cheats

## Database Manipulation in Python

The following code creates a databas with a variants collection.

```python
from pymongo import MongoClient
from datetime import datetime

db_client = MongoClient()
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