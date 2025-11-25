# classifier_utils.py
from sage.all import Link
from wild_mosaics import orientedGaussCode

def jones_unknot(mosaic):
    """
    Check if a mosaic represents the unknot using Jones polynomial.
    
    Args:
        mosaic: A Mosaic object from wild_mosaics.py
        
    Returns:
        bool: True if unknot, False otherwise
        
    Raises:
        Exception: If the number of crossings exceeds 22 (Jones polynomial becomes unreliable)
    """
    if mosaic.numCrossings() > 22:
        raise Exception(f"Jones polynomial cannot reliably detect knottedness. Number of crossings: {mosaic.numCrossings()}")
    
    K = Link(orientedGaussCode(mosaic))
    
    if K.jones_polynomial(algorithm='statesum') == 1:
        return True
    else:
        return False