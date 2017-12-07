import sys
sys.path.append('..')

import databasehelper
from bson.objectid import ObjectId
import configmanager 

DBNAME = "dev"

DB_NAME = configmanager.get_key('DATABASE', 'DatabaseName')
DB_COLLECTION_LOCALAPPS = configmanager.get_key('DATABASE', 'LocalappsCollection')
DB_COLLECTION_GLOBALAPPS = configmanager.get_key('DATABASE', 'GlobalappsCollection')
DB_COLLECTION_RULES = configmanager.get_key('DATABASE', 'RulesCollection')
DB_COLLECTION_TEMP_DATASTORE = configmanager.get_key('DATABASE', 'DataStoreCollectionTemp')
INTERVAL = float(configmanager.get_key('INTERVALS', 'RulebaseInterval'))

exit(0)

# Arguments
# data numbers and connecting mode (0: neighbors, 1: chains)

# Drop global apps


# Add global apps


# Drop local apps

# Add local apps
db = databasehelper.get_database(DB_NAME)
col = databasehelper.get_collection(db, DB_COLLECTION_LOCALAPPS)
globalapp_info = find_globalapp_info(globalapp_id)

new_app['module_name'] = globalapp_info['module_name']
new_app['global_app_id'] = globalapp_id
new_app["_id"] = ObjectId(new_app["_id"])

result = databasehelper.insert(col, new_app)
__load_localapp(str(new_app['_id']))

# Drop devices

# Add devices

# Drop linkage rules

# App linkage rules
# neighbors or chains
