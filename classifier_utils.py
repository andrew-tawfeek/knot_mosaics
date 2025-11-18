# classifier_utils.py
import regina
import snappy
from sage.all import Link
from wild_mosaics import orientedGaussCode

def check_unknot(knot_pd):
    """
    Check if a knot (given by PD code) is an unknot.
    """
    try:
        L = snappy.Link(knot_pd)
        M = L.exterior()
        T = regina.Triangulation3(M)
        return T.isSolidTorus()
    except Exception as e:
        print(f"Error in check_unknot: {e}")
        raise