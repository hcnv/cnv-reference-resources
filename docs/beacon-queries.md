# Beacon CNV Queries

!!! Note "Beacon Project Query Documentation"

    The Beacon [project's documentation](http://docs.genomebeacons.org/variant-queries/#beacon-range-queries) includes examples for current queries enabling
    discovery of CNVs (in resources supporting these formats).


## Bracket queries

### Beacon parameters

* In principle the `assemblyId` should not be needed if specifying the refseq ID
* Most beacons probably would go for `assemblyId` + chromosome-style `referenceName` (e.g. `9`)

=== "Beacon v2 POST snippet"

    ```json
    "g_variant": {
        "assemblyId": "GRCh38",
        "end": [21967753, 22500000],
        "referenceName": "refseq:NC_000009.12",
        "start": [21500000, 21975098],
        "variantType": "EFO:0030067"
    }
    ```

=== "Beacon v2 GET"

    ```
    ?assemblyId=GRCh38&referenceName=refseq:NC_000009.12&start=21500000,21975098&end=21967753,22500000&variantType=EFO:0030067
    ```


### MongoDB translation

The parameters in the MongoDB query represent a "VRSified standard model" structure - YMMV.
Also, this example shows the expansion of the basic "deletion" code (EFO:0030067)
into all its child terms.

```json
"query": {
    "$and": [
        {"location.sequence_id": "refseq:NC_000009.12"},
        {"location.start": {"$gte": 21500000}},
        {"location.start": {"$lt": 21975098}},
        {"location.end": {"$gte": 21967753}},
        {"location.end": {"$lt": 22500000}},
        {"variantState.id": {
                "$in": [
                    "EFO:0030067",
                    "EFO:0030068",
                    "EFO:0020073",
                    "EFO:0030069"
                ]
            }
        }
    ]
}
```