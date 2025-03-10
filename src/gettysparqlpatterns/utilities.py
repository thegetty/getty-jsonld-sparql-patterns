class SPARQLPatternsError(ValueError):
    pass


class NoSuchPatternError(SPARQLPatternsError):
    pass


class RequiredParametersMissingError(SPARQLPatternsError):
    pass


class NoSPARQLEndpointSetError(SPARQLPatternsError):
    pass


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
