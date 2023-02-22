class TNLUnidentifiedToken(Exception):
    """Used when an unknown token is encountered"""
    pass

class TNLSyntax(Exception):
    """Used when the TNL syntax is incorrect"""
    pass

class TNLUndeclaredVariable(Exception):
    """Used when a variable is assigned a value before being declared"""