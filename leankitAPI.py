#!flask/bin/python

from flask import Flask, jsonify

app = Flask(__name__)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def getFishTankTemp (ProbeSerialNum):

    # Output probably looks like this:
    # b1 01 4b 46 7f ff 0f 10 8d : crc=8d YES
    # b1 01 4b 46 7f ff 0f 10 8d t=27062
    # The t= portion is the temp in celcius, in other words 27.062 C
    # Here's how I original did it:
    # cat dev-file | grep 't=' | awk -F= '{printf ("(%d/1000*1.8)+32\n", $2)}' | bc -l | awk '{printf ("%.2f\n", $1)}'

    tempF = float(0.0);
#    ProbeSerialNum='28-00000463f2a4'
    deviceFile = "/sys/bus/w1/devices/%s/w1_slave" % ProbeSerialNum;
    with open(deviceFile, 'r') as content_file:
        for line in content_file:
            # Grab the line which contains "t="
            if "t=" in line:
                # Split the line by '=', get second argument, and convert to integer
                celcius = int(line.split('=')[1]);
                # Convert to F
                tempF = (celcius / 1000.0 * 1.8) + 32
    return tempF;


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Endpoint for Tank Water Temp
# @app.route is a Python Decorator, modifies the function directly below it
# Decorators wrap a python function, modifying it's behavior

@app.route('/leankit/list', methods=['GET'])
def return_fishtank_temp():
    # would like to run this:
    # node leankit/get_cards_by_lane.js --accountName https://jnj.leankit.com --boardId 372745411 --printCards --printOptions UPLGTZ  --jsonify
    import subprocess
    jsonString = subprocess.check_output(['/usr/bin/node', 
                                          'leankit/get_cards_by_lane.js', 
                                          '--accountName', 'https://jnj.leankit.com',
                                          '--boardId', '372745411',
                                          '--printCards',
                                          '--printOptions', 'UPLGTZ', 
                                          '--jsonify']);
    import json
    cardsObj = json.loads(jsonString);
    
    del cardsObj[5:]
    return (json.dumps(cardsObj));


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

from flask import abort

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# make sure we don't run accidentally if we get imported by other python script
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5017, debug=False)


# ===============================================================================================
# ==========================   End   ============================================================
# ===============================================================================================
