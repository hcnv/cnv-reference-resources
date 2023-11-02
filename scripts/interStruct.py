
# class Call:

#     def __init__(self, name, data):
#         self.SAMPLENAME = name
#         self.DATA = data

#     def __repr__(self):
#         return 'sample name: {};\t data: {}'.format(self.SAMPLENAME, self.DATA)


# VCF variants and calls
class Variant:


    def __init__(self, chrom, pos, id, ref, alt, qual, filter, info):
        self.CHROM = chrom.split("r")[1]
        self.POS = pos
        self.ID = id
        self.REF = ref
        self.ALT = str(alt)[2:5]
        self.QUAL = qual
        self.FILTER = filter
        self.INFO = info
        self.CALLS = []
        self.PASS = True
        self.VARIANT_INTERNAL_ID = ""
        self.VARIANT_TYPE = ""


    def __repr__(self):
        return 'chro:{}; pos:{}; id:{}; ref:{}; alt:{}; qual:{}; filter:{}; info:{};\ncalls:{}'.format(self.CHROM,
            self.POS, self.ID, self.REF, self.ALT, self.QUAL, self.FILTER, self.INFO, self.CALLS)


    # to traverse nested dictionary keys
    # k is a list of key names
    def nested_dict_get(self, dic, k):
        if len(k) > 1:
            return self.nested_dict_get(dic[k[0]], k[1:])
        else:
            return dic.get(k[0], None)

    # convert a call to the defined schema
    def convertCall(self, definition, schema, call):
        for k,v in definition.items():
            if type(v) == dict:
                schema[k] = {}
                self.convertCall(v, schema[k], call)
            elif type(v) == list:
                if v[0] == 'CALLS':
                    schema[k] = self.nested_dict_get(call, v[1:])
                else:
                    schema[k] = self.nested_dict_get(getattr(self, v[0]), v[1:])
            else:
                schema[k] = getattr(self, v, v)

    # convert the variant to the defined schema
    def convertVariant(self, definition):
        output_struct = []
        for call in self.CALLS:
            schema = {}
            self.convertCall(definition, schema, call)
            output_struct.append(schema)
        return output_struct

class Sample:

    def __init__(self, name):
        self.NAME = name

    def __repr__(self):
        return 'name:'.format(self.NAME)


