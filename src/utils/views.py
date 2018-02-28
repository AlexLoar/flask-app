from os.path import join, dirname, abspath, normpath
import json

from jsonschema.exceptions import ValidationError
from jsonschema import validate


def validate_data(data, schema_name):
    absolute_path = normpath(join(dirname(abspath(__file__)), 'validators/{}.json'.format(schema_name)))

    if not isinstance(data, dict):
        data = json.loads(data)
    try:
        with open(absolute_path) as schema_file:
            schema = json.loads(schema_file.read())
            validate(data, schema)
    except Exception as err:
        raise ValidationError(err.message)
