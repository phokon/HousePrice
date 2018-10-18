import requests
import xml.etree.ElementTree as ET
from peewee import *

ZWS_ID = 'X1-ZWz1ggucbbcd8r_9fxlx'

API_PROPERTY_DETAIL = 'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm'




db = SqliteDatabase('house.db')

def get_property_details(zpid):
    qp = {'zws-id': ZWS_ID, 'zpid':zpid}
    resp = requests.get(API_PROPERTY_DETAIL, params=qp)
    if resp.status_code != 200:
        return None
    return resp.content


def parse_XML_to_dict(xml_file, attrib_set):
    dict = {}
    root = ET.fromstring(xml_file)
    for child in root.iter('*'):
        if child is not None:
            if child.tag in attrib_set:
                dict[child.tag] = child.text
    print (dict)
    return dict



def create_table():
    db.connect()
    db.drop_tables([House])
    db.create_tables([House])

house_attrib = set(['street', 'zipcode', 'city', 'state', 'latitude', 'longitude', 'useCode', 'taxAssessmentYear','taxAssessment',
                    'yearBuilt','lotSizeSqFt','finishedSqFt','bedrooms','bathrooms', 'lastSoldDate', 'lastSoldPrice','zestimatePrice','zestimateDate',
                    'numFloors','numRooms','basement','parkingType','coveredParkingSpaces','elementarySchool','middleSchool','highSchool'])



class House(Model):
    zpid = IntegerField(unique=True)
    street = CharField(null=True)
    zipcode = CharField(null=True)
    city = CharField(null=True)
    state = CharField(null=True)
    latitude = DoubleField(null=True)
    longitude = DoubleField(null=True)
    useCode = CharField(null=True)
    taxAssessmentYear = SmallIntegerField(null=True)
    taxAccessment = DoubleField(null=True)
    yearBuilt = SmallIntegerField(null=True)
    lotSizeSqFt = IntegerField(null=True)
    finishedSqFt = IntegerField(null=True)
    bedrooms = SmallIntegerField(null=True)
    bathrooms = DoubleField(null=True)
    lastSoldDate = DateField(null=True)
    lastSoldPrice = IntegerField(null=True)
    zestimatePrice = IntegerField(null=True)
    zestimateDate = DateField(null=True)

    # additional details
    numFloors = SmallIntegerField(null=True)
    numRooms = SmallIntegerField(null=True)
    basement = CharField(null=True)
    parkingType = CharField(null=True)
    coveredParkingSpaces = SmallIntegerField(null=True)
    elementarySchool = CharField(null=True)
    middleSchool = CharField(null=True)
    highSchool = CharField(null=True)

    def set_attributes(self, initial_dict):
        for key in initial_dict:
            setattr(self, key, initial_dict[key])

    class Meta:
        # this model uses "house.db" database
        database = db






def test_parse_xml():
    response = get_property_details(51731365)
    initial_dict = parse_XML_to_dict(response, house_attrib)
    house = House(zpid=51731365)
    house.set_attributes(initial_dict)
    try:
        house.save()
    except:
        print('Duplicated entry.')

create_table()
test_parse_xml()