"""
Classifier microservice for knot unknot detection.
This should run in the knot_mosaics repository with SageMath environment.

Run with: sage -python classifier_service.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

# Import SageMath and classifier dependencies
try:
    from sage.all import Link
    import regina
    import snappy
    sys.path.insert(0, '.')
    from wild_mosaics import Mosaic, orientedGaussCode
    from classifier_utils import check_unknot  # Import from your utils file
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure to run this with: sage -python classifier_service.py")
    sys.exit(1)

app = Flask(__name__)
CORS(app)


def check_unknot(knot_pd):
    """
    Check if a knot (given by PD code) is an unknot.
    
    Args:
        knot_pd: Planar diagram code (list of 4-element lists)
        
    Returns:
        bool: True if unknot, False if knotted
    """
    try:
        L = snappy.Link(knot_pd)
        M = L.exterior()
        T = regina.Triangulation3(M)
        return T.isSolidTorus()
    except Exception as e:
        print(f"Error in check_unknot: {e}")
        raise


def classify_mosaic(mosaic_matrix):
    """
    Classify a mosaic matrix as unknot or knotted.
    
    Args:
        mosaic_matrix: 2D list of integers representing the mosaic
        
    Returns:
        dict: {"is_unknot": bool, "pd_code": list}
    """
    try:
        # Create Mosaic object from matrix
        M = Mosaic(mosaic_matrix)
        
        # Check for trivial cases (fewer than 3 crossings typically means unknot)
        num_crossings = M.numCrossings()
        if num_crossings < 3:
            return {
                "is_unknot": True,
                "reason": "trivial_few_crossings",
                "num_crossings": num_crossings,
                "pd_code": None
            }
        
        # Convert: Mosaic -> Gauss code -> Sage Link -> PD code
        gauss_code = orientedGaussCode(M)
        sage_link = Link(gauss_code)
        pd_code = sage_link.pd_code()
        
        # Check if unknot using topology
        is_unknot = check_unknot(pd_code)
        
        return {
            "is_unknot": bool(is_unknot),
            "reason": "topology_check",
            "num_crossings": num_crossings,
            "pd_code": [[int(x) for x in crossing] for crossing in pd_code]
        }
        
    except Exception as e:
        raise ValueError(f"Error classifying mosaic: {str(e)}")


@app.route('/api/classify', methods=['POST'])
def classify():
    """
    Classify a knot mosaic.
    
    Expected JSON:
    {
        "mosaic": [[0, 5, 6, 0], [5, 9, 10, 6], ...]
    }
    
    Returns:
    {
        "is_unknot": true/false,
        "reason": "trivial_few_crossings" or "topology_check",
        "num_crossings": 5,
        "pd_code": [[...], ...]
    }
    """
    try:
        data = request.get_json(force=True)
        
        if 'mosaic' not in data:
            return jsonify({"error": "Missing 'mosaic' field"}), 400
        
        mosaic_matrix = data['mosaic']
        
        # Validate input
        if not isinstance(mosaic_matrix, list) or not all(isinstance(row, list) for row in mosaic_matrix):
            return jsonify({"error": "Mosaic must be a 2D list"}), 400
        
        result = classify_mosaic(mosaic_matrix)
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "knot-classifier",
        "sage_available": True
    }), 200


if __name__ == '__main__':
    print("Starting Knot Classifier Service...")
    print("Make sure wild_mosaics.py is in the same directory!")
    app.run(debug=True, host='0.0.0.0', port=5001)