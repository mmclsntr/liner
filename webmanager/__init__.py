from flask import Flask, render_template, request, redirect, url_for
from flask_classy import FlaskView, route
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..') 
from appmanager import AppManager
from devicemanager import DeviceManager

class WebManager:
  app = Flask(__name__)
  __dbname = ''

  def __init__(self, dbname: str):
    self.__dbname = dbname
    DeviceView.register(self.app)
    DeviceView.set_dbname(dbname)

  def run(self, debug: bool):
    self.app.debug = debug
    self.app.run(host='0.0.0.0')

  @app.route('/')
  def index():
    title = 'Central Manager'
    return render_template('index.html', title = title)


  ### Connector Setting ###
  class ConnectorView(FlaskView):
    @route('/connectors')
    def connector():
      return render_template('connectors.html')

  
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
    return render_template('device.html', device=deviceinfo, local_apps=applist)

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
    devicelist = devicemanager.list_devices()
    # TODO
    print(request.form)
    return redirect(url_for('DeviceView:list'))
  
  @route('/<int:deviceid>/app/<int:localappid>', methods=['GET', 'POST'])
  def localapp(self, deviceid, localappid):
    appmanager = AppManager(self.dbname)
    appinfo = appmanager.find_localapp_info(localappid)
    return render_template('device_app.html', islocal=True, app=appinfo, deviceid=deviceid)

  @route('/<int:deviceid>/app/<int:localappid>/save/', methods=['POST'])
  def localapp_save(self, deviceid, localappid):
    appmanager = AppManager(self.dbname)
    devicemanager = DeviceManager(appmanager, self.dbname)
    devicelist = devicemanager.list_devices()
    # TODO
    print(request.form)
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
  
  @route('/<int:deviceid>/store/<int:localappid>/save/', methods=['POST'])
  def globalapp_save(self, deviceid, localappid):
    appmanager = AppManager(self.dbname)
    devicemanager = DeviceManager(appmanager, self.dbname)
    devicelist = devicemanager.list_devices()
    # TODO
    print(request.form)
    return redirect(url_for('DeviceView:get', deviceid=deviceid))
  

  @route('/<int:deviceid>/app/<int:localappid>/datastore/', methods=['GET', 'POST'])
  def datastore(self, deviceid, localappid):
    return render_template('device_datastore.html')

  @classmethod
  def set_dbname(cls, dbname):
    cls.dbname = dbname

if __name__ == '__main__':
  webmanager = WebManager('dev')
  webmanager.run(True)
