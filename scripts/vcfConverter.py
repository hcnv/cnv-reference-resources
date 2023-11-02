import vcf
import yaml
from interStruct import Variant, Sample

EFO_dict = { 'EFO:0030067': 'copy number loss',
  'EFO:0030068': 'low-level copy number los' ,
  'EFO:0030069': 'complete genomic deletion',
  'EFO:0030070': 'copy number gain' ,
  'EFO:0030071': 'low-level copy number gain' ,
  'EFO:0030072': 'high-level copy number gain' ,
  'EFO:0030073': 'focal genome amplification' }
easy_EFO_dict = {"DEL":'EFO:0030067',"DUP":"EFO:0030070"}

# turn VCF data into objects
# functions for converting the VCF data into customized data structures
class vcfConverter:

    def __init__(self, vcf_file):

        vcf_reader = vcf.Reader(open(vcf_file, 'r'))

        # parse samples
        self.samples = {}
        for sample in vcf_reader.samples:
            self.samples[sample] = Sample(name = sample)

        # parse variants and calls
        self.variants = []

        for record in vcf_reader:
            variant = Variant(record.CHROM, 
                              record.POS, 
                              record.ID, 
                              record.REF, 
                              record.ALT,
                              record.QUAL, 
                              record.FILTER, 
                              record.INFO)
            variant.VARIANT_INTERNAL_ID=str(record.CHROM)+":"+str(record.POS-1)+"-"+str(record.ID).split(":")[3].split("-")[1]+":"+easy_EFO_dict[variant.ALT]

            variant.VARIANT_TYPE=easy_EFO_dict[variant.ALT]
          

            for call in record.samples:
                variant.CALLS.append({'NAME':call.sample, 'DATA':call.data._asdict()})
            self.variants.append(variant)
            if int(variant.CALLS[0]["DATA"]["CN"]) ==1:
                variant.VARIANT_INTERNAL_ID = str(record.CHROM) + ":" + str(record.POS - 1) + "-" + \
                                              str(record.ID).split(":")[3].split("-")[1] + ":" + 'EFO:0030068'
            if int(variant.CALLS[0]["DATA"]["CN"]) ==0:
                variant.VARIANT_INTERNAL_ID = str(record.CHROM) + ":" + str(record.POS - 1) + "-" + \
                                              str(record.ID).split(":")[3].split("-")[1] + ":" + 'EFO:0030069'
            if int(variant.CALLS[0]["DATA"]["CN"]) >2 and int(variant.CALLS[0]["DATA"]["CN"]) <4:
                variant.VARIANT_INTERNAL_ID = str(record.CHROM) + ":" + str(record.POS - 1) + "-" + \
                                              str(record.ID).split(":")[3].split("-")[1] + ":" + 'EFO:0030071'
            if int(variant.CALLS[0]["DATA"]["CN"]) >4:
                variant.VARIANT_INTERNAL_ID = str(record.CHROM) + ":" + str(record.POS - 1) + "-" + \
                                              str(record.ID).split(":")[3].split("-")[1] + ":" + 'EFO:0030072'


    # convert the VCF data into a data structure described by a definition file.
    def convertVariants(self, def_file):
        with open(def_file, 'r') as fi:
            definition = yaml.load(fi, Loader=yaml.FullLoader)

        struct = []
        for variant in self.variants:
            struct.extend(variant.convertVariant(definition))

        return struct


