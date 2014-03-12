import pytesla
import osmapi
import urllib2
from time import sleep

class Commands(object):
    @classmethod
    def open_sunroof(cls, vehicle_obj, pct):
        vehicle_obj.sun_roof_control('move', pct)

    @classmethod
    def close_sunroof(cls, vehicle_obj):
        vehicle_obj.sun_roof_control('close')

    @classmethod
    def get_gui_settings(cls, vehicle_obj):
        print vehicle_obj.gui_settings

    @classmethod
    def get_drive_state(cls, vehicle_obj):
        print vehicle_obj.drive_state

    @classmethod
    def get_latlong(cls, vehicle_obj):
        return vehicle_obj.drive_state['latitude'], vehicle_obj.drive_state['longitude']


class OSM(object):
    def __init__(self, api_uri='api06-dev.openstreetmap.org', 
                       username=u"pete2212", password=None):
	self.api_uri = api_uri
	self.username = username
	self.password = password
#        self.api = osmapi.OsmApi(api, username, password)

    def create_node(self, lat, lon, note=None, tag=None):
	api = osmapi.OsmApi(self.api_uri, self.username, self.password)
	api.ChangesetCreate({u"comment": u"Master of the Universe!"})
	print api.NodeCreate({u"lon": lon, u"lat": lat, u"tag": {"TESLA!!"}})
	api.ChangesetClose()


def login(user, pw):
    mycar = pytesla.Connection(user, pw).vehicles()[0]
    return mycar

def send_req(timeout=30, msg=None):
    connected = False
    #retrieve car instance
    cred = {}
    f = open('pw_file.pw')
    for l in f:
        l = l.split('=')
        cred[l[0].strip()] = l[1].strip()
    car = login(cred['user'], cred['pw'])
    tries = 0
    inst = login
    while( tries <= timeout and connected == False):
        try:
            connected = car.wake_up()
	    break
	except urllib2.HTTPError, err:
            if err.code == 408:
                if tries % 3 == 0:
                    print 'connection timed out, trying again'
            else:
                print 'received http error[%s] logging in, trying again' % (err) 
	except Exception, e:
            print 'received error[%s] logging in, trying again' % (e)
            print type(e)
        if connected is not None:
            tries = tries + 1
            sleep(1)
    if connected is not True:
        print 'Failed to contact Tesla'
send_req()
#load pw info
#cred = {}
#f = open('pw_file.pw')
#for l in f:
#    l = l.split('=')
#    cred[l[0].strip()] = l[1].strip()

#osmap = OSM(password=cred['pw'])
#print cred
#mycar = pytesla.Connection(cred['user'], cred['pw']).vehicles()[0]
#mycar.wake_up()
#print mycar.honk_horn()
#print mycar.charge_state
#print mycar.vehicle_state
#print Commands().open_sunroof(mycar, 30)
#Commands().get_gui_settings(mycar)
#Commands().get_drive_state(mycar)
#lat, lon = Commands().get_latlong(mycar)
#osmap.create_node(lat, lon)
#Commands().close_sunroof(mycar)
