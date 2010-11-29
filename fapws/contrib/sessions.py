#    Copyright (C) 2009 William.os4y@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import datetime, time
try:
    import cPickle as pickle
except:
    import pickle
import os
import binascii

class Session:
    def __init__(self,sessiondb,datetime_fmt="%Y-%m-%d %H:%M:%S"):
        self.sessiondb=sessiondb # must have a get method abd return dictionary like object with sessionid, strdata and expiration_date
        self.datetime_fmt=datetime_fmt
    def getdata(self):
        "return the python objected associated or None in case of expiration"
        exp=self.sessiondb.get('expiration_date',None)
        if not exp:
            return None
        if type(exp)==type(datetime.datetime(2011,1,1)):
            expdate=exp
        elif type(exp)==type("string") or type(exp)==type(u"string"):
            expdate=datetime.datetime.fromtimestamp(time.mktime(time.strptime(exp, self.datetime_fmt))) 
        else:
            raise ValueError, "expiration_Date must be a datetime object or a string (%s)" % self.datetime_fmt
        if expdate>datetime.datetime.now():
            #expired
            return None
        else:
            strdata=str(self.sessiondb['strdata'])
            data=pickle.loads(strdata)
            return data
    def setdata(self, data):
        strdata=pickle.dumps(data)
        if not self.sessiondb['sessionid']:
            self.newid()
        self.sessiondb['strdata']=strdata
        self.sessiondb['expiration_date']=self._getdate()
    def newid(self):
        sessid=binascii.hexlify(os.urandom(12))
        self.sessiondb['sessionid']=sessid
        self.sessiondb['expiration_date']=self._getdate()
    def _getdate(self):
        return datetime.datetime.now().strftime(self.datetime_fmt)

