class SPARQLPatternsError(ValueError):
    pass


class NoSuchPatternError(SPARQLPatternsError):
    pass


class NoPatternsFoundError(NoSuchPatternError):
    """Could not find a suitable pattern list to import."""

    pass


class PatternNotSetError(SPARQLPatternsError):
    pass


class RequiredParametersMissingError(SPARQLPatternsError):
    pass


class NoSPARQLEndpointSetError(SPARQLPatternsError):
    pass
