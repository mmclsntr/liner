from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys,os
from bson.objectid import ObjectId
import json

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..') 
import nodemanager
import devicemanager
import rulebaselinkage
import configmanager


DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')

class WebManager:
  app = Flask(__name__)
  
  def run_server(self):
    self.app.run(host='0.0.0.0')

  def __init__(self, debug: bool):
    self.app.debug = debug

  def start(self):
    self.app.run(host='0.0.0.0')

  @app.route('/')
  def index():
    title = 'Central Manager'
    return render_template('index.html', title = title)

### Device Setting
  @app.route('/devices/', methods=['GET', 'POST'])
  def devices():
    devicelist = devicemanager.list_devices()
    nodelist = nodemanager.list_nodes()
    return render_template('devices.html', devices=devicelist, nodes=nodelist)

  @app.route('/devices/deviceview/', methods=['GET'])
  def devices_deviceview():
    return render_template('device_area.html')
  
  @app.route('/devices/approwview/', methods=['GET'])
  def devices_app_row_view():
    return render_template('device_app_row.html')

  @app.route('/device/<deviceid>/app/<nodeid>', methods=['GET', 'POST'])
  def device_node(deviceid, nodeid):
    appinfo = nodemanager.find_node_info(nodeid)
    return render_template('device_app.html', islocal=True, node=nodeinfo, deviceid=deviceid)

  @app.route('/device/<deviceid>/app/<nodeid>/save/', methods=['POST'])
  def device_node_save(deviceid, nodeid):
    nodeinfo = nodemanager.find_node_info(nodeid)
    node_moduleinfo = nodemanager.find_node_module_info(nodeinfo['node_module_id'])
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    configs = []
    for config in node_moduleinfo['required_configs']:
      cf = {}
      cf['name'] = config['name']
      convertstr = str(config['type']) + '("' + str(request.form['config:' + str(config['name'])]) + '")'
      cf['value'] = eval(convertstr)
      cf['type'] = config['type']
      configs.append(cf)
    info['configs'] = configs
    print(info)
    nodemanager.update_node_info(nodeid, info)
    return redirect('/devices/')

  @app.route('/device/<deviceid>/app/<nodeid>/delete/', methods=['GET', 'POST'])
  def device_node_delete(deviceid, nodeid):
    nodemanager.delete(nodeid)
    devicemanager.delete_nodeid(deviceid, nodeid)
    return redirect('/devices/')

  @app.route('/device/<deviceid>/store/', methods=['GET', 'POST'])
  def device_appstore(deviceid):
    nodelist = nodemanager.list_node_modules()
    return render_template('store.html', deviceid=deviceid, nodes=nodelist)

  @app.route('/device/<deviceid>/store/<node_moduleid>', methods=['GET', 'POST'])
  def device_node_module(deviceid, node_moduleid):
    nodeinfo = nodemanager.find_node_module_info(node_moduleid)
    return render_template('device_app.html', islocal=False, node=nodeinfo, deviceid=deviceid)
  
  @app.route('/device/<deviceid>/store/<node_moduleid>/save/', methods=['POST'])
  def device_node_module_save(deviceid, node_moduleid):
    node_moduleinfo = nodemanager.find_node_module_info(node_moduleid)
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    info['module_name'] = node_moduleinfo['module_name']
    if 'readtype' in node_moduleinfo:
      info['readtype'] = node_moduleinfo['readtype']
    if 'writetype' in node_moduleinfo:
      info['writetype'] = node_moduleinfo['writetype']
    info['node_module_id'] = node_moduleid
    info["_id"] = str(ObjectId())
    configs = []
    for config in node_moduleinfo['required_configs']:
      cf = {}
      cf['name'] = config['name']
      convertstr = str(config['type']) + '("' + str(request.form['config:' + str(config['name'])]) + '")'
      cf['value'] = eval(convertstr)
      cf['type'] = config['type']
      configs.append(cf)
    info['configs'] = configs
    nodemanager.add(node_moduleid, info)

    deviceinfo = devicemanager.find_device_info(deviceid)
    if not 'nodes' in deviceinfo:
      deviceinfo['nodes'] = []
    deviceinfo['nodes'].append(str(info["_id"]))
    del deviceinfo["_id"]
    devicemanager.update(deviceid, deviceinfo)
    return redirect("/devices/")
  
  @app.route('/device/<deviceid>/app/<nodeid>/control/', methods=['GET', 'POST'])
  def device_app_control(deviceid, nodeid):
    nodeinfo = nodemanager.find_node_info(nodeid)
    return render_template('device_app_control.html', node=nodeinfo, deviceid=deviceid)

  @app.route('/device/<deviceid>/app/<nodeid>/datastore/', methods=['GET', 'POST'])
  def device_app_datastore(deviceid, nodeid):
    nodeinfo = nodemanager.find_node_info(nodeid)
    return render_template('device_app_datastore.html', node=nodeinfo, deviceid=deviceid)


### Rulebase connector ###
  @app.route('/connectors/', methods=['GET', 'POST'])
  def connectors():
    listrules = rulebaselinkage.list_rules()
    nodelist = nodemanager.list_nodes()
    return render_template('rulebaseconnector.html', connectors=listrules, nodes=nodelist)

  @app.route('/connectors/connectorview/', methods=['GET'])
  def connectors_connectorview():
    return render_template('connector_area.html')

### API ###
  @app.route('/api/connector/<connectorid>/save/', methods=['POST'])
  def api_connector_id_save(connectorid):
    configs = request.json
    query = configs
    _id = connectorid

    if connectorid == "new":
      query["_id"] = str(ObjectId())
      _id = query["_id"]
      rulebaselinkage.add(query)
    else: 
      rulebaselinkage.update(connectorid, query)

    return jsonify({"_id": _id})
    
  @app.route('/api/connector/<connectorid>/remove/', methods=['DELETE'])
  def api_connector_id_remove(connectorid):
    rulebaselinkage.delete(connectorid)

    return jsonify({"_id": connectorid})
  
  @app.route('/api/device/<deviceid>/save/', methods=['POST'])
  def api_device_id_save(deviceid):
    configs = request.json
    query = configs
    _id = deviceid

    if deviceid == "new":
      query["_id"] = str(ObjectId())
      _id = query["_id"]
      devicemanager.add(query)
    else: 
      devicemanager.update(deviceid, query)

    return jsonify({"_id": _id})
    
  @app.route('/api/device/<deviceid>/remove/', methods=['DELETE'])
  def api_device_id_remove(deviceid):
    devicemanager.delete_apps(deviceid)
    devicemanager.delete(deviceid)

    return jsonify({"_id": deviceid})

  @app.route('/api/app/<nodeid>', methods=['GET'])
  def api_app_id(nodeid):
    node = nodemanager.find_node_info(nodeid)
    node["_id"] = str(node["_id"])
    return jsonify(node)
  
  @app.route('/api/app/<nodeid>/save/', methods=['POST'])
  def api_app_id_save(nodeid):
    req = request.json
    node_moduleid = req['node_module_id']
    if nodeid != 'new':
      nodeinfo = nodemanager.find_node_info(nodeid)
    node_moduleinfo = nodemanager.find_node_module_info(nodeinfo['node_module_id'])
    query = {}
    query['name'] = request.form['name']
    query['note'] = request.form['note']
    configs = []
    for config in node_moduleinfo['required_configs']:
      cf = {}
      cf['name'] = config['name']
      convertstr = str(config['type']) + '("' + str(request.form['config:' + str(config['name'])]) + '")'
      cf['value'] = eval(convertstr)
      cf['type'] = config['type']
      configs.append(cf)
    info['configs'] = configs
    nodemanager.update_node_info(nodeid, info)
    return jsonify(node)
  
  @app.route('/api/app/<nodeid>/read/', methods=['GET'])
  def api_app_id_read(nodeid):
    value = nodemanager.read_node_value(nodeid)
    return jsonify({"value": value})

  @app.route('/api/app/<nodeid>/write/', methods=['POST'])
  def api_app_id_write(nodeid):
    req = request.json
    if "value" in req and "type" in req:
      value = nodemanager.write_node_value(nodeid, eval(req["type"] + "('" + req["value"] + "')"))
      return jsonify({"code": 200})
    else:
      return jsonify({"code": 400})

  @app.route('/api/app/<nodeid>/datastore/', methods=['GET'])
  def api_app_id_datastore(nodeid):
    num = request.args.get("num");
    values = nodemanager.datastore(nodeid, int(num));
    return jsonify(values);


webmanager= WebManager(False)
def run_server():
  webmanager.start()    

def kill_server():
  webmanager.stop()

#if __name__ == '__main__':
#  webmanager = WebManager('dev')
#  webmanager.run(True)
