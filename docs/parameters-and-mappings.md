# hCNV Parameters and Mappings to Output format

## Collected Parameters

### Variants data

* CNV type (DUP, DEL...)
    - translated to EFO terms using CN count values
* referenceName
    - chromosome translated to refseq id w/ prefix
* start
    - left-shifted since 0-based coordinates instead of VCFs 1-based
* end
    - from INFO
* CN count
    - from call field
* assemblyId
    - from header (GRCh38)

### Metadata

* sample id
* donor id? different?
* sequencing platform
* sequencing library / model (?)
* sex
* ethnicity ...
* geographic provenance
* external references, e.g. biosamples collection ID (as CURIE) and associated
  publication(s)

## Parameter Output Mappings

!!! Warning "Output Model"
    The information below just gives some indications about the way these are handled
    in the Beacon default model and its Progenetix variant. However, the current idea
    is to go directly for a representation through Phenopackets (which has many similarities
    to Beacon v2 but a different unified wrapper model).

### Beacon v2 Default Model for `genomicVariation`

* [**Beacon v2 default model source**](https://github.com/ga4gh-beacon/beacon-v2/tree/main/models/src/beacon-v2-default-model)
* [**Beacon v2 default model documentation**](http://docs.genomebeacons.org/models/)

Beacon v2 provides a default model with its main data entities `individual`,
`biosample`, `analysis`, `run` and `genomicVariation`. The parameters needed for
an hCNV reference resource potentially map to all of those entities; e.g.

* donor sex  => `individual.sex`

### Progenetix `bycon` parameter mappings

The Progenetix implementation of the Beacon API - through the [`bycon`](https://github.com/progenetix/bycon/)
stack - closely adheres internally to the Beacon v2 default model. Specifically,
records are stored in document formats described in JSON Schema with overall correspondance
to the standard Beacon models, and stored in a MongoDB database with per schema
collections (`individuals`, `biosamples`, `callsets` and `variants` as well as helper
collections for e.g. ontologies or genome lookups).

For data I/O the `bycon` package contains a mapping file which allows to map data from
columnar (_i.e._ tab delimited) input files to the corresponding attributes in the
document schemas.

#### Example `bycon` parameter mappings

``` yaml
  genomicVariant:
    type: object
    parameters:
      variant_id:
        db_key: id
        indexed: True
        compact: True
        computed: True
      variant_internal_id:
        type: string
        db_key: variant_internal_id
        indexed: True
        compact: True
        computed: True
      callset_id:
      	description: |
      		The bycon model uses `callset` to store
      		information corresponding to Beacon's `analysis`
      		and `run` entities.
        type: string
        db_key: callset_id
        indexed: True
        compact: True
      biosample_id:
        type: string
        db_key: biosample_id
        indexed: True
        compact: True
      individual_id:
        type: string
        db_key: individual_id
        indexed: True
        compact: True
      sequence_id:
        type: string
        db_key: location.sequence_id
        indexed: True
        compact: True
      reference_name:
        type: string
        db_key: location.chromosome
        indexed: True
        compact: True
      start:
        type: integer
        db_key: location.start
        indexed: True
        compact: True
      end:
        type: integer
        db_key: location.end
        indexed: True
        compact: True
      variant_state_id:
        type: string
        db_key: variant_state.id
        indexed: True
        compact: True
      variant_state_label:
        type: string
        db_key: variant_state.label
        compact: True
      reference_bases:
        type: string
        db_key: reference_sequence
        indexed: True
        compact: True
      alternate_bases:
        type: string
        db_key: sequence
        indexed: True
        compact: True
      annotation_derived:
        type: boolean
        db_key: info.annotation_derived
        default: False
        indexed: True
      aminoacid_changes:
        type: array
        items: string
        db_key: molecular_attributes.aminoacid_changes
        indexed: True
      genomic_hgvs_id:
        type: string
        db_key: identifiers.genomicHGVS_id
        indexed: True

      # special pgxseg columns

      log2:
        db_key: info.cnv_value
        type: number
      variant_type:
        type: string
        db_key: variant_type

```



