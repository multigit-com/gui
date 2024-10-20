import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

@app.route('/api/execute', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command')
    input_data = data.get('input')
    
    script_path = os.path.join(SCRIPTS_DIR, f"{command}.py")
    
    if not os.path.exists(script_path):
        return jsonify({'error': 'Unknown command'})
    
    result = subprocess.run(['python', script_path, input_data], capture_output=True, text=True)
    
    if result.returncode == 0:
        return jsonify({'success': True, 'output': result.stdout})
    else:
        return jsonify({'success': False, 'error': result.stderr})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
