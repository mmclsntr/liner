from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView, route
import sys,os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..') 
import appmanager
import devicemanager
import rulebaseconnectormanager
import configmanager

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')

class WebManager:
  app = Flask(__name__)

  def __init__(self):
    pass

  def run(self, debug: bool):
    self.app.debug = debug
    self.app.run(host='0.0.0.0')

  @app.route('/')
  def index():
    title = 'Central Manager'
    return render_template('index.html', title = title)

### Device Setting

  @app.route('/device/<deviceid>', methods=['GET', 'POST'])
  def device(deviceid):
    deviceinfo = devicemanager.find_device_info(deviceid)
    applist = appmanager.list_localapps()
    return render_template('device.html', isnew=False, device=deviceinfo, local_apps=applist)

  @app.route('/device/new/', methods=['GET', 'POST'])
  def device_new():
    deviceinfo = {}
    applist = appmanager.list_localapps()
    return render_template('device.html', isnew=True, device=deviceinfo, local_apps=applist)

  @app.route('/device/list/', methods=['GET', 'POST'])
  def device_list():
    devicelist = devicemanager.list_devices()
    applist = appmanager.list_localapps()
    return render_template('devices.html', devices=devicelist, local_apps=applist)

  @app.route('/device/<deviceid>/save/', methods=['POST'])
  def device_save(deviceid):
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    devicemanager.update(deviceid, info)
    return redirect(url_for('DeviceView:list'))
  
  @app.route('/device//new/save/', methods=['POST'])
  def device_new_save():
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    devicemanager.add(info)
    return redirect(url_for('DeviceView:list'))
  
  @app.route('/device/<deviceid>/delete/', methods=['GET', 'POST'])
  def device_delete(deviceid):
    devicemanager.delete(deviceid)
    return redirect(url_for('DeviceView:list'))
  
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
    appmanager.update_app_info(localappid, info)
    return redirect(url_for('DeviceView:get', deviceid=deviceid))

  @app.route('/device/<deviceid>/app/<localappid>/delete/', methods=['GET', 'POST'])
  def device_localapp_delete(deviceid, localappid):
    appmanager.delete(localappid)
    return redirect(url_for('DeviceView:get', deviceid=deviceid))

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
    info['device_id'] = deviceid
    info['module_name'] = globalappinfo['module_name']
    info['global_app_id'] = globalappid
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
    return redirect(url_for('DeviceView:get', deviceid=deviceid))
  

  @app.route('/device/<deviceid>/app/<localappid>/datastore/', methods=['GET', 'POST'])
  def device_datastore(deviceid, localappid):
    return render_template('device_datastore.html')


### Connector Setting ###
  @app.route('/connector/<connectorid>', methods=['GET', 'POST'])
  def connector_get(connectorid):
    rule = rulebaseconnectormanager.find_rule(connectorid)
    return render_template('connector.html', isnew=False, connector=rule)

  @app.route('/connector/<connectorid>/save/', methods=['GET', 'POST'])
  def connector_save(connectorid):
    configs = {}
    configs['name'] = request.form['name']
    configs['event'] = {
      'nodename': request.form['event:nodename'],
      'operator': request.form['event:operator'],
      'value': request.form['event:value']
    }
    configs['actions'] = []
    i = 0
    size = len(request.form.getlist('action:nodename[]'))
    action_nodenames = request.form.getlist('action:nodename[]')
    action_values = request.form.getlist('action:value[]')
    while i < size:
      if action_nodenames[i] == '':
        break
      action = {
        'nodename': action_nodenames[i],
        'value': action_values[i]
      }
      configs['actions'].append(action)
      i += 1
    rulebaseconnectormanager.update(connectorid, configs)
    return redirect(url_for('ConnectorView:list'))

  @app.route('/connector/<connectorid>/delete/', methods=['GET', 'POST'])
  def connector_delete(connectorid):
    rulebaseconnectormanager.delete(connectorid)
    return redirect(url_for('ConnectorView:list'))

  @app.route('/connector/new/', methods=['GET', 'POST'])
  def connector_new():
    return render_template('connector.html', isnew=True)

  @app.route('/connector/new/save/', methods=['GET', 'POST'])
  def connector_new_save():
    configs = {}
    configs['name'] = request.form['name']
    configs['event'] = {
      'nodename': request.form['event:nodename'],
      'operator': request.form['event:operator'],
      'value': request.form['event:value']
    }
    configs['actions'] = []
    i = 0
    size = len(request.form.getlist('action:nodename[]'))
    action_nodenames = request.form.getlist('action:nodename[]')
    action_values = request.form.getlist('action:value[]')
    while i < size:
      if action_nodenames[i] == '':
        break
      action = {
        'nodename': action_nodenames[i],
        'value': action_values[i]
      }
      configs['actions'].append(action)
      i += 1
    rulebaseconnectormanager.add(configs)
    return redirect(url_for('ConnectorView:list'))

  @app.route('/connector/list/', methods=['GET', 'POST'])
  def connector_list():
    listrules = rulebaseconnectormanager.list_rules()
    return render_template('connectors.html', connectors=listrules)

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
    configs = request.get_json();
    rulebaseconnectormanager.update(connectorid, configs)
    return redirect(url_for('ConnectorView:list'))
    
  

#if __name__ == '__main__':
#  webmanager = WebManager('dev')
#  webmanager.run(True)
