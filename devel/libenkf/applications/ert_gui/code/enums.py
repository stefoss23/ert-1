
class enumtype(type):
    def __call__(cls, *args, **kwargs):
        newtype = super(enumtype, cls).__call__(*args, **kwargs)
        newtype.__getitem__ = classmethod(enumtype.__getitem__)
        return newtype

    def __getitem__(cls, item):
        """All enums can be accessed with the subscript operator, using the name or value as key"""
        v = cls.resolveValue(item)
        if v is None:
            return cls.resolveName(item)
        else:
            return v

#        if isinstance(item, long) or isinstance(item, int):
#            return cls.resolveValue(item)
#        else:
#            return cls.resolveName(item)

class enum:
    """
    A base class for enums.
    All enums support the subscript operator as a class method. The value or the name can be used as key/index.
    The subscript operator uses the resolveName and resolveValue functions as basis.
    """
    __metaclass__ = enumtype

    _enums = {}  #This contains all sub classed enums! {class : [list of enums], ...}
    def __init__(self, name, value):
        self.name = name
        self.value = value

        if not enum._enums.has_key(self.__class__):
            enum._enums[self.__class__] = []

        enum._enums[self.__class__].append(self)

    @classmethod
    def values(cls):
        """Returns a list of the created enums for a class."""
        return enum._enums[cls]

    @classmethod
    def resolveName(cls, name):
        """Finds an enum based on name. Ignores the case of the name. Returns None if not found."""
        for e in enum._enums[cls]:
            if e.name.lower() == name.lower():
                return e
        return None

    @classmethod
    def resolveValue(cls, value):
        """
        Returns the enum with the specified value.
        If several enums have the same value the first will be returned
        """
        for e in enum._enums[cls]:
            if e.value == value:
                return e
        return None

    def __add__(self, other):
        """Two enums can be added together returning the sum of the value fields"""
        if isinstance(other, self.__class__):
            return self.value + other.value
        else:
            raise NotImplemented


    def __and__(self, other):
        """Bitwise and of two enums or an enum and a long or int."""
        if isinstance(other, self.__class__):
            return self.value & other.value
        elif isinstance(other, long) or isinstance(other, int):
            return self.value & other
        else:
            raise NotImplemented

    def __rand__(self, other):
        return self.__and__(other)

    def __str__(self):
        return self.name

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if isinstance(other, long) or isinstance(other, int):
            return self.value == other
        else:
            return self.value == other.value

    def __hash__(self):
        return hash("%s : %i" % (self.name, self.value))

#    @classmethod
#    def __getitem__(cls, item):
#        if isinstance(item, long) or isinstance(item, int):
#            cls.resolveValue(cls, item)
#        else:
#            cls.resolveName(cls, item)


#-------------------------------------------------------------------
#    enum implementations
#-------------------------------------------------------------------

class ert_state_enum(enum):
    """Defined in enkf_types.h"""
    FORECAST=None
    ANALYZED=None
    BOTH=None

#ert_state_enum.UNDEFINED = ert_state_enum("Undefined", 0)
#ert_state_enum.SERIALIZED = ert_state_enum("Serialized", 1)
ert_state_enum.FORECAST = ert_state_enum("Forecast", 2)
ert_state_enum.ANALYZED = ert_state_enum("Analyzed", 4)
ert_state_enum.BOTH = ert_state_enum("Both", 6)


class enkf_impl_type(enum):
    """Defined in enkf_types.h"""
    #INVALID = 0
    #IMPL_TYPE_OFFSET = 100
    #STATIC = 100
    FIELD = None
    GEN_KW = None
    SUMMARY = None
    GEN_DATA = None
    #MAX_IMPL_TYPE = 113  #! not good to have several with same value, resolveValue fails!!!

enkf_impl_type.FIELD = enkf_impl_type("Field", 104)
enkf_impl_type.GEN_KW = enkf_impl_type("Keyword", 107)
enkf_impl_type.SUMMARY = enkf_impl_type("Summary", 110)
enkf_impl_type.GEN_DATA = enkf_impl_type("Data", 113)


class ert_job_status_type(enum):
    """These "enum" values are all copies from the header file "basic_queue_driver.h"."""
    # Observe that the status strings are available from the function: libjob_queue.job_queue_status_name( status_code )
    NOT_ACTIVE  = None
    LOADING     = None
    WAITING     = None
    SUBMITTED   = None
    PENDING     = None
    RUNNING     = None
    DONE        = None
    EXIT        = None
    RUN_OK      = None
    RUN_FAIL    = None
    ALL_OK      = None
    ALL_FAIL    = None
    USER_KILLED = None
    USER_EXIT   = None

ert_job_status_type.NOT_ACTIVE = ert_job_status_type("JOB_QUEUE_NOT_ACTIVE", 1)
ert_job_status_type.LOADING = ert_job_status_type("JOB_QUEUE_LOADING", 2)
ert_job_status_type.WAITING = ert_job_status_type("JOB_QUEUE_WAITING", 4)
ert_job_status_type.SUBMITTED = ert_job_status_type("JOB_QUEUE_SUBMITTED", 8)
ert_job_status_type.PENDING = ert_job_status_type("JOB_QUEUE_PENDING", 16)
ert_job_status_type.RUNNING = ert_job_status_type("JOB_QUEUE_RUNNING", 32)
ert_job_status_type.DONE = ert_job_status_type("JOB_QUEUE_DONE", 64)
ert_job_status_type.EXIT = ert_job_status_type("JOB_QUEUE_EXIT", 128)
ert_job_status_type.RUN_OK = ert_job_status_type("JOB_QUEUE_RUN_OK", 256)
ert_job_status_type.RUN_FAIL = ert_job_status_type("JOB_QUEUE_RUN_FAIL", 512)
ert_job_status_type.ALL_OK = ert_job_status_type("JOB_QUEUE_ALL_OK", 1024)
ert_job_status_type.ALL_FAIL = ert_job_status_type("JOB_QUEUE_ALL_FAIL", 2048)
ert_job_status_type.USER_KILLED = ert_job_status_type("JOB_QUEUE_USER_KILLED", 4096)
ert_job_status_type.USER_EXIT = ert_job_status_type("JOB_QUEUE_USER_EXIT", 8192)


class gen_data_file_format(enum):
    #defined in gen_data_config.h 
    #GEN_DATA_UNDEFINED = 0
    ASCII          = None
    ASCII_TEMPLATE = None
    BINARY_DOUBLE  = None
    BINARY_FLOAT   = None

    INPUT_TYPES  = None
    OUTPUT_TYPES = None

gen_data_file_format.ASCII = gen_data_file_format("ASCII", 1)
gen_data_file_format.ASCII_TEMPLATE = gen_data_file_format("ASCII_TEMPLATE", 2)
gen_data_file_format.BINARY_DOUBLE = gen_data_file_format("BINARY_DOUBLE", 3)
gen_data_file_format.BINARY_FLOAT = gen_data_file_format("BINARY_FLOAT", 4)

gen_data_file_format.INPUT_TYPES = [gen_data_file_format.ASCII,
                                    gen_data_file_format.BINARY_FLOAT,
                                    gen_data_file_format.BINARY_DOUBLE]

gen_data_file_format.OUTPUT_TYPES = [gen_data_file_format.ASCII,
                                     gen_data_file_format.ASCII_TEMPLATE,
                                     gen_data_file_format.BINARY_FLOAT,
                                     gen_data_file_format.BINARY_DOUBLE]

class field_type(enum):
    ECLIPSE_RESTART = None
    ECLIPSE_PARAMETER = None
    GENERAL = None

field_type.ECLIPSE_RESTART = field_type("Dynamic", 1)
field_type.ECLIPSE_PARAMETER = field_type("Parameter", 2)
field_type.GENERAL = field_type("General", 3)


class truncation_type(enum):
    TRUNCATE_NONE = None
    TRUNCATE_MIN = None
    TRUNCATE_MAX = None

truncation_type.TRUNCATE_NONE = truncation_type("TRUNCATE_NONE", 0)
truncation_type.TRUNCATE_MIN = truncation_type("TRUNCATE_MIN", 1)
truncation_type.TRUNCATE_MAX = truncation_type("TRUNCATE_MAX", 2)

#print enum._enums