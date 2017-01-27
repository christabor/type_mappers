"""A spec and code to implement the spec.

The spec defines a generic mapper for types to other types,
which can be used for validation, code generation and more.
"""

from decimal import Decimal

from datetime import date
from datetime import datetime

import sqlalchemy
import wtforms

try:
    # Py3 only.
    from enum import Enum
except ImportError:
    Enum = None

try:
    # Py3 uses unicode for str.
    unicode
except NameError:
    unicode = str

vanilla = {
    # Numbers
    'int': int,
    'decimal': Decimal,
    'float': float,
    'number': int,
    'num': int,
    'int32': int,
    'int64': int,
    'uint32': int,
    'uint64': int,
    'double': float,
    'long': float,

    # Strings
    'str': str,
    'string': str,
    'unicode': unicode,

    # Booleans
    'true': bool,
    'false': bool,
    'bool': bool,

    # Dates
    'time': datetime,
    'datetime': datetime,
    'date': date,

    # Binary
    'file': bytes,
    'blob': bytes,
    'binary': bytes,
    'bytes': bytes,

    # Password
    'password': str,

    # Multi-choice
    'enum': Enum,

    # Configs/serialized formats - TODO: how best to map these.
    'pickle': None,
    'pkl': None,
    'json': None,
    'yaml': None,
}
sqlalchemy_mapper = {
    # Numbers
    'int': sqlalchemy.Integer,
    'decimal': sqlalchemy.Float,
    'float': sqlalchemy.Float,
    'number': sqlalchemy.Integer,
    'num': sqlalchemy.Integer,
    'int32': sqlalchemy.SmallInteger,
    'int64': sqlalchemy.BigInteger,
    'uint32': sqlalchemy.SmallInteger,
    'uint64': sqlalchemy.BigInteger,
    'double': sqlalchemy.Float,
    'long': sqlalchemy.BigInteger,

    # Strings
    'str': sqlalchemy.String,
    'string': sqlalchemy.String,
    'unicode': sqlalchemy.Unicode,

    # Booleans
    'true': sqlalchemy.Boolean,
    'false': sqlalchemy.Boolean,
    'bool': sqlalchemy.Boolean,

    # Dates
    'time': sqlalchemy.Time,
    'datetime': sqlalchemy.DateTime,
    'date': sqlalchemy.Date,

    # Binary
    'file': sqlalchemy.BLOB,
    'blob': sqlalchemy.BLOB,
    'binary': sqlalchemy.Binary,
    'bytes': sqlalchemy.Binary,

    # Configs/serialized formats
    'pickle': sqlalchemy.PickleType,
    'pkl': sqlalchemy.PickleType,
    'json': sqlalchemy.types.JSON,

    # Multi-choice
    'enum': sqlalchemy.Enum,
}
factoryboy_mapper = {
}
wtform_mapper = {
    # Numbers
    'int': wtforms.IntegerField,
    'decimal': wtforms.DecimalField,
    'float': wtforms.DecimalField,  # Not using floatfield atm
    'number': wtforms.IntegerField,
    'num': wtforms.IntegerField,
    'int32': wtforms.IntegerField,
    'int64': wtforms.IntegerField,
    'uint32': wtforms.IntegerField,
    'uint64': wtforms.DecimalField,
    'double': wtforms.IntegerField,
    'long': wtforms.IntegerField,

    # Strings
    'str': wtforms.TextField,
    'string': wtforms.TextField,
    'unicode': wtforms.TextField,

    # Booleans
    'true': wtforms.BooleanField,
    'false': wtforms.BooleanField,
    'bool': wtforms.BooleanField,

    # Dates
    'time': wtforms.DateTimeField,
    'datetime': wtforms.DateTimeField,
    'date': wtforms.DateField,

    # Binary
    'file': wtforms.FileField,
    'blob': wtforms.FileField,
    'binary': wtforms.FileField,
    'bytes': wtforms.FileField,

    # Password
    'password': wtforms.PasswordField,

    # Multi-choice
    'enum': wtforms.SelectField,

    # Configs/serialized formats
    'pickle': wtforms.TextAreaField,
    'pkl': wtforms.TextAreaField,
    'json': wtforms.TextAreaField,
    'yaml': wtforms.TextAreaField,
}
all_maps = {
    'vanilla': vanilla,
    'wtforms': wtform_mapper,
    'sqlalchemy': sqlalchemy_mapper,
    'factoryboy': factoryboy_mapper,
}


def get_context_field(fieldtype, context):
    """Get the right field for a field type and context label."""
    fieldtype = fieldtype.lower()
    try:
        typ = all_maps[context][fieldtype]
        if typ is None:
            raise NotImplementedError(
                'Type: "{}" for "{}" has '
                'not been implemented'.format(fieldtype, context))
    except KeyError:
        return None
