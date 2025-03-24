import json
from importlib.resources import files, as_file

import gettysparqlpatterns.patterns

source = files(gettysparqlpatterns.data).joinpath("archival_patterns.json")
with as_file(source) as jdoc:
    patternlist = json.loads(jdoc)
