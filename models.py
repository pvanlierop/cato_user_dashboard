from datetime import datetime
from lib2to3.pytree import Base
from pydantic import BaseModel

class RemoteUser(BaseModel):
    id: str
    name: str
    email: str
    phonenumber: str
    version: str
    uptime: datetime
    devicename: str
    osversion: str
    ostype: str
    popname: str
    remoteip: str
    countrycode: str
    countryname: str
    city: str
    state: str
    provider: str
    latitude: str
    longitude: str
    officemode: bool
    connectivitystats: str
    ip: str