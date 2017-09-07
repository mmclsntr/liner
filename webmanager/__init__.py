from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView, route
import sys,os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..') 
from appmanager import AppManager
from devicemanager import DeviceManager
from rulebaseconnectormanager import RuleBaseConnectorManager

class WebManager:
  app = Flask(__name__)
  __dbname = ''

  def __init__(self, dbname: str):
    self.__dbname = dbname
    DeviceView.register(self.app)
    DeviceView.set_dbname(dbname)
    ConnectorView.register(self.app)
    ConnectorView.set_dbname(dbname)

  def run(self, debug: bool):
    self.app.debug = debug
    self.app.run(host='0.0.0.0')

  @app.route('/')
  def index():
    title = 'Central Manager'
    return render_template('index.html', title = title)

  
### Device Setting ###
class DeviceView(FlaskView):
  route_base = '/device'
  dbname = ''

  @route('/<int:deviceid>', methods=['GET', 'POST'])
  def get(self, deviceid):
    appmanager = AppManager(self.dbname)
    devicemanager = DeviceManager(appmanager, self.dbname)
    deviceinfo = devicemanager.find_device_info(deviceid)
    applist = appmanager.list_localapps()
    return render_template('device.html', isnew=False, device=deviceinfo, local_apps=applist)

  @route('/new/', methods=['GET', 'POST'])
  def new(self):
    appmanager = AppManager(self.dbname)
    deviceinfo = {}
    applist = appmanager.list_localapps()
    return render_template('device.html', isnew=True, device=deviceinfo, local_apps=applist)

  @route('/list/', methods=['GET', 'POST'])
  def list(self):
    appmanager = AppManager(self.dbname)
    devicemanager = DeviceManager(appmanager, self.dbname)
    devicelist = devicemanager.list_devices()
    applist = appmanager.list_localapps()
    return render_template('devices.html', devices=devicelist, local_apps=applist)

  @route('/<int:deviceid>/save/', methods=['POST'])
  def device_save(self, deviceid):
    appmanager = AppManager(self.dbname)
    devicemanager = DeviceManager(appmanager, self.dbname)
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    devicemanager.update(deviceid, info)
    return redirect(url_for('DeviceView:list'))
  
  @route('/new/save/', methods=['POST'])
  def device_new_save(self):
    appmanager = AppManager(self.dbname)
    devicemanager = DeviceManager(appmanager, self.dbname)
    info = {}
    info['name'] = request.form['name']
    info['note'] = request.form['note']
    devicemanager.add(info)
    return redirect(url_for('DeviceView:list'))
  
  @route('/<int:deviceid>/delete/', methods=['GET', 'POST'])
  def device_delete(self, deviceid):
    appmanager = AppManager(self.dbname)
    devicemanager = DeviceManager(appmanager, self.dbname)
    devicemanager.delete(deviceid)
    return redirect(url_for('DeviceView:list'))
  
  @route('/<int:deviceid>/app/<int:localappid>', methods=['GET', 'POST'])
  def localapp(self, deviceid, localappid):
    appmanager = AppManager(self.dbname)
    appinfo = appmanager.find_localapp_info(localappid)
    return render_template('device_app.html', islocal=True, app=appinfo, deviceid=deviceid)

  @route('/<int:deviceid>/app/<int:localappid>/save/', methods=['POST'])
  def localapp_save(self, deviceid, localappid):
    appmanager = AppManager(self.dbname)
    localappinfo = appmanager.find_localapp_info(localappid)
    globalappinfo = appmanager.find_globalapp_info(int(localappinfo['global_app_id']))
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

  @route('/<int:deviceid>/app/<int:localappid>/delete/', methods=['GET', 'POST'])
  def localapp_delete(self, deviceid, localappid):
    appmanager = AppManager(self.dbname)
    appmanager.delete(localappid)
    return redirect(url_for('DeviceView:get', deviceid=deviceid))

  @route('/<int:deviceid>/store/', methods=['GET', 'POST'])
  def store(self, deviceid):
    appmanager = AppManager(self.dbname)
    applist = appmanager.list_globalapps()
    return render_template('store.html', deviceid=deviceid, apps=applist)

  @route('/<int:deviceid>/store/<int:globalappid>', methods=['GET', 'POST'])
  def globalapp(self, deviceid, globalappid):
    appmanager = AppManager(self.dbname)
    appinfo = appmanager.find_globalapp_info(globalappid)
    return render_template('device_app.html', islocal=False, app=appinfo, deviceid=deviceid)
  
  @route('/<int:deviceid>/store/<int:globalappid>/save/', methods=['POST'])
  def globalapp_save(self, deviceid, globalappid):
    appmanager = AppManager(self.dbname)
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
  

  @route('/<int:deviceid>/app/<int:localappid>/datastore/', methods=['GET', 'POST'])
  def datastore(self, deviceid, localappid):
    return render_template('device_datastore.html')

  @classmethod
  def set_dbname(cls, dbname):
    cls.dbname = dbname


### Connector Setting ###
class ConnectorView(FlaskView):
  route_base = '/connector'
  dbname = ''

  @route('/<int:connectorid>', methods=['GET', 'POST'])
  def get(self, connectorid):
    appmanager = AppManager(self.dbname)
    rulebaseconnectormanager = RuleBaseConnectorManager(appmanager, self.dbname)
    rule = rulebaseconnectormanager.find_rule(connectorid)
    return render_template('connector.html', isnew=False, connector=rule)

  @route('/<int:connectorid>/save/', methods=['GET', 'POST'])
  def connector_save(self, connectorid):
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
    appmanager = AppManager(self.dbname)
    rulebaseconnectormanager = RuleBaseConnectorManager(appmanager, self.dbname)
    rulebaseconnectormanager.update(connectorid, configs)
    return redirect(url_for('ConnectorView:list'))

  @route('/<int:connectorid>/delete/', methods=['GET', 'POST'])
  def connector_delete(self, connectorid):
    appmanager = AppManager(self.dbname)
    rulebaseconnectormanager = RuleBaseConnectorManager(appmanager, self.dbname)
    rulebaseconnectormanager.delete(connectorid)
    return redirect(url_for('ConnectorView:list'))

  @route('/new/', methods=['GET', 'POST'])
  def new(self):
    return render_template('connector.html', isnew=True)

  @route('/new/save/', methods=['GET', 'POST'])
  def new_save(self):
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
    appmanager = AppManager(self.dbname)
    rulebaseconnectormanager = RuleBaseConnectorManager(appmanager, self.dbname)
    rulebaseconnectormanager.add(configs)
    return redirect(url_for('ConnectorView:list'))

  @route('/list/', methods=['GET', 'POST'])
  def list(self):
    appmanager = AppManager(self.dbname)
    rulebaseconnectormanager = RuleBaseConnectorManager(appmanager, self.dbname)
    listrules = rulebaseconnectormanager.list_rules()
    return render_template('connectors.html', connectors=listrules)

  @classmethod
  def set_dbname(cls, dbname):
    cls.dbname = dbname

if __name__ == '__main__':
  webmanager = WebManager('dev')
  webmanager.run(True)
