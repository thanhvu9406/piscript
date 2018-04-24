import zklib
import requests
import json
import os
from datetime import datetime
module_path = os.path.dirname(os.path.realpath(__file__))
log_path = module_path + '/piscript.log'

import logging
logging.basicConfig(filename=log_path, level=logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

print requests.__version__
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def send_to_server(location, url='https://www.dhamedic.vn/post/hr_attendance', datas={}):
    logging.info('Send to %s datas: %s'%(str(url), str(len(datas))))
    datas_str = json.dumps({
        'attendances': datas,
        'location': location
    }, ensure_ascii=False)
    r = requests.post(url, data=datas_str)
    return r

def get_attendance(zk):
    logging.info('Get Attendance')

    res = zk.connect()
    error = ''
    att_results = []
    if res:
        zk.enableDevice()
        user = zk.getUser()
        attendance = zk.getAttendance()
        if (attendance):
            zk.enableDevice()
            zk.disconnect()
            return attendance
        else:
            error = 'Unable to get the attendance log, please try again later.'
    else:
        raise 'Unable to connect, please check the parameters and network connections.'


if __name__ == "__main__":
    try:
        os.system('sudo chmod +rw %s'%log_path)
    except:
        pass

    logging.info('%s Started'%now)
    arrgs = {}
    config_path = os.path.dirname(os.path.realpath(__file__)) + '/config.conf'
    with open(config_path) as f:
        content = f.readlines()
        for line in content:
            temp = line.rstrip().split('=')
            arrgs[temp[0].strip()] = temp[1].strip()

    zk = zklib.zklib.ZKLib(arrgs['machine_ip'], int(arrgs['machine_port']), timeout=int(arrgs['time_out']))
    attendances = get_attendance(zk)
    if attendances:
        send_to_server(arrgs['location'], url=arrgs['server_url'], datas=attendances)


