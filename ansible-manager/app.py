from flask import Flask, render_template, request
import yaml
import os
import re
import subprocess
import requests

app = Flask(__name__)
rootDirectory = os.path.abspath(os.path.join(app.root_path, os.pardir))

@app.route('/', methods=['GET']) # , 'POST'
def root():
  print(request.method)
  #return render_template('index.html')
  return 'Hi'

@app.route('/deploy', methods=['GET'])
def deploy():
  ver = request.args['v']
  global rootDirectory
  playbookFile = f'playbook_v{ver}.yaml'
  playbook = os.path.join(rootDirectory, playbookFile)
  subprocess.run(['ansible-playbook',playbook])
  msg = f'Running deploy for v{ver}...'
  return msg

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)

#@app.route('/saveConfig', methods=['GET', 'POST'])
#def saveConfig():
#  global config
#  config.clear()
#  config['realm'] = request.form.get('realm')
#  config['accessToken'] = request.form.get('accessToken')
#  saveConfigFile(config)
#  subprocess.run(['helm', 'install', '-f',  otelColPath, '--generate-name', 'splunk-otel-collector-chart/splunk-otel-collector'])
#  return {}