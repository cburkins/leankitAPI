#!flask/bin/python

# import libraries from local flask library
from flask import Flask, jsonify
# Library for Cross Origin Resource Sharing
# one-time to load: flask/bin/pip install -U flask-cors
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# allows CORS for all domains on all routes
CORS(app)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Endpoint to list all Leankit cards on our board
# @app.route is a Python Decorator, modifies the function directly below it
# Decorators wrap a python function, modifying it's behavior
@app.route('/leankit/list', methods=['GET'])
def return_fishtank_temp():
    # would like to run this:
    # node leankit/get_cards_by_lane.js --accountName https://jnj.leankit.com --boardId 372745411 --printCards --printOptions UPLGTZ  --jsonify
    import subprocess
    jsonString = subprocess.check_output(['/usr/bin/node', 
                                          'leankit/get_cards_by_lane.js', 
                                          '--boardId', '372745411',
                                          '--printCards',
                                          '--printOptions', 'ABCDFGPYZTWELIVU', 
                                          '--jsonify']);
    import json
    cardsObj = json.loads(jsonString);
    
    # Truncate the card list to 5
    #del cardsObj[5:]

    return (json.dumps(cardsObj));
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - -  Main   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# make sure we don't run accidentally if we get imported by other python script
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1433, debug=False, threaded=True)


# ===============================================================================================
# ==========================   End   ============================================================
# ===============================================================================================
