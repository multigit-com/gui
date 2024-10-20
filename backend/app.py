import os
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

@app.route('/api/execute', methods=['POST'])
def execute_command():
    try:
        data = request.json
        command = data.get('command')
        input_data = data.get('input')
        
        script_path = os.path.join(SCRIPTS_DIR, f"{command}.py")
        
        if not os.path.exists(script_path):
            return jsonify({'error': 'Unknown command'}), 400
        
        # Ensure input_data is a list
        if not isinstance(input_data, list):
            input_data = [input_data]
        
        result = subprocess.run(['python', script_path] + input_data, capture_output=True, text=True)
        
        # Log the action
        subprocess.run(['python', os.path.join(SCRIPTS_DIR, 'audit_log.py'), command] + input_data)
        
        if result.returncode == 0:
            return jsonify({'success': True, 'output': result.stdout})
        else:
            return jsonify({'success': False, 'error': result.stderr}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audit-log', methods=['GET'])
def get_audit_log():
    try:
        result = subprocess.run(['python', os.path.join(SCRIPTS_DIR, 'audit_log.py')], capture_output=True, text=True)
        return jsonify(json.loads(result.stdout))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
