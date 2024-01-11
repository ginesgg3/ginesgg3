# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 19:07:53 2023

@author: Ginés González Guirado
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, Float, String, SmallInteger

Base = declarative_base()

class GinesGonzalez(Base):
    __tablename__ = 'gines_gonzalez'
    __mapper_args__ = {
        'include_properties': ['ph','site','date','elevacion_solar',
                               'distancia_TS','presion','temperatura'],
    }

    ph = Column('ph', Integer, primary_key=True)
    site = Column('site', String(50))
    date = Column('date', DateTime)
    elevacion_solar = Column('elevacion_solar', Float)
    distancia_TS = Column('distancia_TS', Float)
    presion = Column('presion', Float)
    temperatura = Column('temperatura', Float)
    



class CaePhotometer(Base):
    __tablename__ = 'cae_photometer'
    __mapper_args__ = {
        'include_properties': ['id'],
    }

    id = Column('id', Integer, primary_key=True)
    



class CaeStation(Base):
    __tablename__ = 'cae_station'
    __mapper_args__ = {
        'include_properties': ['name','longitude','latitude','altitude'],
    }

    name = Column('name', String(50), primary_key=True)
    longitude = Column('longitude', Float)
    latitude = Column('latitude', Float)
    altitude = Column('altitude', Float)
    



class CmlDataScene(Base):
    __tablename__ = 'cml_data_scene'
    __mapper_args__ = {
        'include_properties': ['ph', 'date',
                               'filename', 'type',
                               'offset', 'number']
    }
    ph = Column('ph', Integer, primary_key=True)
    date = Column('date', DateTime, primary_key=True)
    filename = Column('filename', String(200))
    type = Column('type', String)
    offset = Column('offset', SmallInteger)
    number = Column('number', SmallInteger)




class CmlDataSceneParameter(Base):
    __tablename__ = 'cml_data_scene_parameter'
    __mapper_args__ = {
        'include_properties': ['ph','date','number','filename','key','value'],
    }

    ph = Column('ph', Integer, primary_key=True)
    date = Column('date', DateTime, primary_key=True)
    number = Column('number', SmallInteger, primary_key=True)
    filename = Column('filename', String(200))
    key = Column('key', String(50))
    value = Column('value', Float)
    

    
class CmlInstallation(Base):
    __tablename__ = 'cml_installation'
    __mapper_args__ = {
        'include_properties': ['photometer', 'site', 'first', 'last'],
    }

    photometer = Column('photometer', Integer, primary_key=True)
    site = Column('site', String(50), primary_key=True)
    first = Column('first', DateTime, primary_key=True)
    last = Column('last', DateTime, primary_key=True)
    



