class SPARQLResponseObj(str):
    """Catch-all subclass, in case of strange types in the responses (blank nodes?)"""

    def __new__(cls, value, type, datatype=None):
        obj = str.__new__(cls, value)
        obj.sparql_type = type
        obj.datatype = datatype
        return obj

    def __repr__(self):
        if self.datatype:
            return f'SPARQLLiteral("{super().__repr__()}", sparql_type={self.sparql_type!r}, datatype="{self.datatype!r}")'
        return (
            f"SPARQLResponseObj({super().__repr__()}, sparql_type={self.sparql_type!r})"
        )


class SPARQLURI(str):
    """Subclass a string so that for all intents and purposes it is a string but the
    class indicates that this is a URI from a SPARQL response rather than a plain string
    """

    def __new__(cls, value):
        obj = str.__new__(cls, value)
        obj.sparql_type = "URI"
        obj.datatype = None
        return obj

    def __repr__(self):
        return f"SPARQLURI(URI <{super().__repr__()}>)"


class SPARQLLiteral(str):
    """Subclass a string so that for all intents and purposes it is a string but the
    class indicates that this is a plain string from a SPARQL response. Why this exists is so that
    it is safe to look for the attribute 'sparql_type' in any SPARQL response value"""

    def __new__(cls, value, datatype=None):
        obj = str.__new__(cls, value)
        obj.sparql_type = "Literal"
        obj.datatype = datatype
        return obj

    def __repr__(self):
        if self.datatype:
            return (
                f'SPARQLLiteral("{super().__repr__()}", datatype="{self.datatype!r}")'
            )
        return f'SPARQLLiteral("{super().__repr__()}")'


def parsed_sparql_response(resp, stype):
    match resp:
        case {"head": {}, "boolean": resp}:
            return resp
        case {"head": {"vars": [*_]}, "results": {"bindings": [*results]}}:
            # assume that any results returned is a truthy response
            if stype == "count":
                match results:
                    case [
                        {
                            "count": {
                                "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                                "type": "literal",
                                "value": count,
                            }
                        }
                    ]:
                        return int(count)

            # Process the response as a standard SELECT response
            parsed_results = []
            for resultrow in results:
                row = {}
                for k, v in resultrow.items():
                    match v:
                        case {
                            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
                            "type": "literal",
                            "value": value,
                        }:
                            row[k] = int(value)
                        case {"type": "uri", "value": value}:
                            row[k] = SPARQLURI(value)
                        case {"type": "literal", "value": value, **other}:
                            datatype = other.get("datatype")
                            row[k] = SPARQLLiteral(value, datatype)
                        case {"type": othertype, "value": value, **other}:
                            datatype = other.get("datatype")
                            row[k] = SPARQLResponseObj(
                                value, othertype, datatype=datatype
                            )
                parsed_results.append(row)
            return parsed_results
        case other:
            return other
