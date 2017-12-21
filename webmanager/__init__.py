from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys,os
from bson.objectid import ObjectId
import json

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..') 
import appmanager
import devicemanager
import rulebaseconnectormanager
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
    applist = appmanager.list_localapps()
    return render_template('devices.html', devices=devicelist, localapps=applist)

  @app.route('/devices/deviceview/', methods=['GET'])
  def devices_deviceview():
    return render_template('device_area.html')
  
  @app.route('/devices/approwview/', methods=['GET'])
  def devices_app_row_view():
    return render_template('device_app_row.html')

  @app.route('/device/<deviceid>/app/<localappid>', methods=['GET', 'POST'])
  def device_localapp(deviceid, localappid):
    appinfo = appmanager.find_localapp_info(localappid)
    return render_template('device_app.html', islocal=True, app=appinfo, deviceid=deviceid)

  @app.route('/device/<deviceid>/app/<localappid>/save/', methods=['POST'])
  def device_localapp_save(deviceid, localappid):
    localappinfo = appmanager.find_localapp_info(localappid)
    globalappinfo = appmanager.find_globalapp_info(localappinfo['global_app_id'])
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    configs = []
    for config in globalappinfo['required_configs']:
      cf = {}
      cf['name'] = config['name']
      convertstr = str(config['type']) + '("' + str(request.form['config:' + str(config['name'])]) + '")'
      cf['value'] = eval(convertstr)
      cf['type'] = config['type']
      configs.append(cf)
    info['configs'] = configs
    print(info)
    appmanager.update_app_info(localappid, info)
    return redirect('/devices/')

  @app.route('/device/<deviceid>/app/<localappid>/delete/', methods=['GET', 'POST'])
  def device_localapp_delete(deviceid, localappid):
    appmanager.delete(localappid)
    devicemanager.delete_appid(deviceid, localappid)
    return redirect('/devices/')

  @app.route('/device/<deviceid>/store/', methods=['GET', 'POST'])
  def device_appstore(deviceid):
    applist = appmanager.list_globalapps()
    return render_template('store.html', deviceid=deviceid, apps=applist)

  @app.route('/device/<deviceid>/store/<globalappid>', methods=['GET', 'POST'])
  def device_globalapp(deviceid, globalappid):
    appinfo = appmanager.find_globalapp_info(globalappid)
    return render_template('device_app.html', islocal=False, app=appinfo, deviceid=deviceid)
  
  @app.route('/device/<deviceid>/store/<globalappid>/save/', methods=['POST'])
  def device_globalapp_save(deviceid, globalappid):
    globalappinfo = appmanager.find_globalapp_info(globalappid)
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    info['module_name'] = globalappinfo['module_name']
    info['readtype'] = globalappinfo['readtype']
    info['writetype'] = globalappinfo['writetype']
    info['global_app_id'] = globalappid
    info["_id"] = str(ObjectId())
    configs = []
    for config in globalappinfo['required_configs']:
      cf = {}
      cf['name'] = config['name']
      convertstr = str(config['type']) + '("' + str(request.form['config:' + str(config['name'])]) + '")'
      cf['value'] = eval(convertstr)
      cf['type'] = config['type']
      configs.append(cf)
    info['configs'] = configs
    appmanager.add(globalappid, info)

    deviceinfo = devicemanager.find_device_info(deviceid)
    if not 'apps' in deviceinfo:
      deviceinfo['apps'] = []
    deviceinfo['apps'].append(str(info["_id"]))
    del deviceinfo["_id"]
    devicemanager.update(deviceid, deviceinfo)
    return redirect("/devices/")
  
  @app.route('/device/<deviceid>/app/<localappid>/control/', methods=['GET', 'POST'])
  def device_app_control(deviceid, localappid):
    appinfo = appmanager.find_localapp_info(localappid)
    return render_template('device_app_control.html', app=appinfo, deviceid=deviceid)

  @app.route('/device/<deviceid>/app/<localappid>/datastore/', methods=['GET', 'POST'])
  def device_app_datastore(deviceid, localappid):
    appinfo = appmanager.find_localapp_info(localappid)
    return render_template('device_app_datastore.html', app=appinfo, deviceid=deviceid)


### Rulebase connector ###
  @app.route('/connectors/', methods=['GET', 'POST'])
  def connectors():
    listrules = rulebaseconnectormanager.list_rules()
    applist = appmanager.list_localapps()
    return render_template('rulebaseconnector.html', connectors=listrules, localapps=applist)

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
      rulebaseconnectormanager.add(query)
    else: 
      rulebaseconnectormanager.update(connectorid, query)

    return jsonify({"_id": _id})
    
  @app.route('/api/connector/<connectorid>/remove/', methods=['DELETE'])
  def api_connector_id_remove(connectorid):
    rulebaseconnectormanager.delete(connectorid)

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

  @app.route('/api/app/<localappid>', methods=['GET'])
  def api_app_id(localappid):
    localapp = appmanager.find_localapp_info(localappid)
    localapp["_id"] = str(localapp["_id"])
    return jsonify(localapp)
  
  @app.route('/api/app/<localappid>/save/', methods=['POST'])
  def api_app_id_save(localappid):
    req = request.json
    globalappid = req['global_app_id']
    if localappid != 'new':
      localappinfo = appmanager.find_localapp_info(localappid)
    globalappinfo = appmanager.find_globalapp_info(localappinfo['global_app_id'])
    query = {}
    query['name'] = request.form['name']
    query['note'] = request.form['note']
    configs = []
    for config in globalappinfo['required_configs']:
      cf = {}
      cf['name'] = config['name']
      convertstr = str(config['type']) + '("' + str(request.form['config:' + str(config['name'])]) + '")'
      cf['value'] = eval(convertstr)
      cf['type'] = config['type']
      configs.append(cf)
    info['configs'] = configs
    appmanager.update_app_info(localappid, info)
    return jsonify(localapp)
  
  @app.route('/api/app/<localappid>/read/', methods=['GET'])
  def api_app_id_read(localappid):
    value = appmanager.read_app_value(localappid)
    return jsonify({"value": value})

  @app.route('/api/app/<localappid>/write/', methods=['POST'])
  def api_app_id_write(localappid):
    req = request.json
    if "value" in req and "type" in req:
      value = appmanager.write_app_value(localappid, eval(req["type"] + "('" + req["value"] + "')"))
      return jsonify({"code": 200})
    else:
      return jsonify({"code": 400})

  @app.route('/api/app/<localappid>/datastore/', methods=['GET'])
  def api_app_id_datastore(localappid):
    num = request.args.get("num");
    values = appmanager.datastore(localappid, int(num));
    return jsonify(values);


webmanager= WebManager(False)
def run_server():
  webmanagerthread.start()    

def kill_server():
  webmanagerthread.stop()

#if __name__ == '__main__':
#  webmanager = WebManager('dev')
#  webmanager.run(True)
