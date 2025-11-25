# classifier_service.py

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
    sys.path.insert(0, '.')
    from wild_mosaics import Mosaic, orientedGaussCode
    from classifier_utils import jones_unknot
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure to run this with: sage -python classifier_service.py")
    sys.exit(1)

app = Flask(__name__)
CORS(app)


def classify_mosaic(mosaic_matrix):
    """
    Classify a mosaic matrix as unknot or knotted using Jones polynomial.
    
    Args:
        mosaic_matrix: 2D list of integers representing the mosaic
        
    Returns:
        dict: Classification result with is_unknot, reason, and other info
    """
    try:
        # Create Mosaic object from matrix
        M = Mosaic(mosaic_matrix)
        
        # Check for trivial cases
        num_crossings = M.numCrossings()
        
        # If no crossings, it's definitely an unknot
        if num_crossings == 0:
            return {
                "is_unknot": True,
                "reason": "no_crossings",
                "num_crossings": 0,
                "gauss_code": None
            }
        
        # Check if too many crossings for reliable Jones polynomial
        if num_crossings > 22:
            return {
                "is_unknot": None,
                "reason": "too_many_crossings",
                "num_crossings": num_crossings,
                "error": "Jones polynomial is unreliable for knots with more than 22 crossings",
                "gauss_code": None
            }
        
        # Use Jones polynomial to classify
        gauss_code = orientedGaussCode(M)
        is_unknot = jones_unknot(M)
        
        return {
            "is_unknot": bool(is_unknot),
            "reason": "jones_polynomial",
            "num_crossings": num_crossings,
            "gauss_code": gauss_code
        }
        
    except Exception as e:
        raise ValueError(f"Error classifying mosaic: {str(e)}")


@app.route('/api/classify', methods=['POST'])
def classify():
    """
    Classify a knot mosaic using Jones polynomial.
    
    Expected JSON:
    {
        "mosaic": [[0, 5, 6, 0], [5, 9, 10, 6], ...]
    }
    
    Returns:
    {
        "is_unknot": true/false/null,
        "reason": "no_crossings" | "jones_polynomial" | "too_many_crossings",
        "num_crossings": 5,
        "gauss_code": [[...], [...]] or null
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
        "sage_available": True,
        "method": "jones_polynomial"
    }), 200


if __name__ == '__main__':
    print("Starting Knot Classifier Service...")
    print("Using Jones polynomial for knot detection")
    print("Server running on http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)