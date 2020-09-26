from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.conf import settings
import json, os, time, sqlite3

def get_db_info(dbname):
  dbset = {}
  try:
    dbset = settings.DATABASES[dbname]
  except:
    dbset = {
      'ENGINE': '', 'TYPE': '', 'NAME': '', 'USER': '', 'PASSWORD': '', 'HOST': '', 'PORT': '',
    }
  return dbset


def tb_timezone():
  return "SET TIMEZONE to 'Asia/Taipei';"


def get_siteinfo():
  siteinfo = {
    'sitetitle': {
      'en': 'DATA PLATFORM',
      'zh-tw': '資料分析管理系統',
      'zh-cn': '資料分析管理系統'
    },
    'enterinfo': {
      'en': 'Please Enter Your Information',
      'zh-tw': '請輸入帳號資訊',
      'zh-cn': '请输入帐户信息'
    },
    'login': {
      'en': 'Login',
      'zh-tw': '登錄',
      'zh-cn': '登录'
    }
  }
  return siteinfo


def isDigital(val):
  try:
    f = float(val)
  except:
    return False
  return True


def has_auth(user):
  #return True
  if user.is_authenticated == True:
    return True
  return False


def get_apiauth():
  return True


def api_response(msg, cmd=''):
  if cmd != '':
    return {'err': msg, 'cmd': cmd}

  return {'err': msg}


def verify_params(req, lst, exlst=[]):
  params = []
  try:
    if req.method == 'GET':
      params = req.GET
    elif req.method == 'POST':
      body_unicode = req.body.decode('utf-8')
      params = json.loads(body_unicode)
  except:
    pass

  res = {}
  errs = []
  try:
    for item in lst:
      if params.get(item, None) in [None, '']:
        errs.append(item)
      else:
        res.update({item: params.get(item, None)})
  except:
    pass

  msg = ''
  if len(errs) > 0:
    msg = (', ').join(errs) + ' not found'

  try:
    for item in exlst:
      res.update({item: params.get(item, '')})
  except:
    pass

  return {'msg': msg, 'params': res}


def verify_param_exist(req, lst):
  params = []
  try:
    if req.method == 'GET':
      params = req.GET
    elif req.method == 'POST':
      body_unicode = req.body.decode('utf-8')
      params = json.loads(body_unicode)
  except:
    pass

  res = {}
  errs = []
  try:
    for item in lst:
      if params.get(item, None) in [None]:
        errs.append(item)
      else:
        res.update({item: params.get(item, None)})
  except:
    pass

  msg = ''
  if len(errs) > 0:
    msg = (', ').join(errs) + ' not found'

  return {'msg': msg, 'params': res}


def get_api_info(apiurl, params):
  basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  dbfile = os.path.join(basedir, 'cfg.sqlite3')

  sql_string = '''
    SELECT * FROM params WHERE param_name in ('{}')
  '''.format(("', '").join(['apihost_url', apiurl]))

  urls = ''
  method = 'get'
  try:
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute(sql_string)
    columns = [col[0] for col in cursor.description]
    ret = [dict(zip(columns, row)) for row in cursor.fetchall()]

    hostpath = ''
    apipath  = ''
    paramcnt = 0
    for it in ret:
      if it.get('param_name') == 'apihost_url':
        hostpath = it.get('param_value')
      if it.get('param_name') == apiurl:
        apipath = it.get('param_value')
        method = it.get('method')
        paramcnt = it.get('param_count')

    cursor.close()
    conn.close()

    if paramcnt and len(params) >= paramcnt:
      urls = str(hostpath + apipath).format(*params)
    else:
      urls = str(hostpath + apipath)

  except Exception as e:
    pass

  if method == 'both':
    method = 'post'

  return {'urls': urls, 'method': method}


def get_module_info():
  basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  dbfile = os.path.join(basedir, 'cfg.sqlite3')

  sql_string = '''
    SELECT * FROM module order by 'order';
  '''

  modules = []
  try:
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute(sql_string)
    columns = [col[0] for col in cursor.description]
    modules = [dict(zip(columns, row)) for row in cursor.fetchall()]
  except Exception as e:
    pass

  return modules
