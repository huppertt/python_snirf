#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 13:28:35 2020

@author: theodorehuppert
"""


import h5py as h5py
import numpy as np
import re
import colorama
from colorama import Fore, Style
import sys

class data:
    dataTimeSeries = None
    time = None
    measurementList=None

class measurementList:
    sourceIndex=None
    detectorIndex=None
    wavelengthIndex=None
    wavelengthActual=None
    wavelengthEmissionsActual=None
    dataType=None
    dataTypeLabel=None
    dataTypeIndex=None
    sourcePower=None
    detectorGain=None
    moduleIndex=None

class probe:
    wavelengths=None
    wavelengthsEmission=None
    sourcePos2D=None
    sourcePos3D=None
    detectorPos2D=None
    detectorPos3D=None
    frequencies=None
    timeDelays=None
    timeDelayWidths=None
    momentOrder=None
    correlationTimeDelays=None
    correlationTimeDelayWidths=None
    sourceLabels=None
    detectorLabels=None
    landmarkPos2D=None
    landmarkPos3D=None
    landmarkLabels=None

class aux:
    name=None
    dataTimeSeries=None
    time=None
    timeOffSet=None

class stim:
    name=None
    data=None
    

class snirf:
    filename=None
    formatVersion = "1.0"
    data=None
    stim=None
    probe=None
    aux=None
    metaDataTags=None
    
   
def read_from_file(filename):
     fileID = h5py.File(filename, 'r')
     formatVersion=hdfgetdata(fileID,"/formatVersion")
     keys=fileID['/']
     s=[]
     for x in keys:
         if 'nirs' in x:
             a=snirf
             a.formatVersion=formatVersion
             a.probe=read_probe(fileID['/'][x]['probe']);
             a.data=[];
             a.aux=[];
             a.stim=[];
             keys2=fileID['/'][x]
             for x2 in keys2:
                 if 'data' in x2:
                     d = read_data(fileID['/'][x][x2])
                     a.data.append(d)
                 if 'aux' in x2:
                     ax = read_aux(fileID['/'][x][x2])
                     a.aux.append(ax)
                 if 'stim' in x2:
                     ax = read_stim(fileID['/'][x][x2])
                     a.stim.append(ax)   
                     
             a.stim=np.array(a.stim)
             a.data=np.array(a.data)
             a.aux=np.array(a.aux)
             s.append(a)
     if len(s)==1:
         s=s[0]
             
     return s
             
             

def read_data(gID):
    d = data
    
    d.dataTimeSeries =hdfgetdata(gID,'dataTimeSeries')
    d.time=hdfgetdata(gID,'time')
    d.measurementList=[];
    for fld in gID:
        if 'measurementList' in fld:
            d.measurementList=read_measurementList(gID[fld])
    
    d.measurementList=np.array(measurementList)
    
    return d
    
    
def read_probe(gID):
    p=probe
    
    p.wavelengths=hdfgetdata(gID,'wavelengths')
    p.wavelengthsEmission=hdfgetdata(gID,'wavelengthsEmission')
    p.sourcePos2D=hdfgetdata(gID,'sourcePos2D')
    p.sourcePos3D=hdfgetdata(gID,'sourcePos3D')
    p.detectorPos2D=hdfgetdata(gID,'detectorPos2D')
    p.detectorPos3D=hdfgetdata(gID,'detectorPos3D')
    p.frequencies=hdfgetdata(gID,'frequencies')
    p.timeDelays=hdfgetdata(gID,'timeDelays')
    p.timeDelayWidths=hdfgetdata(gID,'timeDelayWidths')
    p.momentOrder=hdfgetdata(gID,'momentOrder')
    p.correlationTimeDelays=hdfgetdata(gID,'correlationTimeDelays')
    p.correlationTimeDelayWidths=hdfgetdata(gID,'correlationTimeDelayWidths')
    p.sourceLabels=hdfgetdata(gID,'sourceLabels')
    p.detectorLabels=hdfgetdata(gID,'detectorLabels')
    p.landmarkPos2D=hdfgetdata(gID,'landmarkPos2D')
    p.landmarkPos3D=hdfgetdata(gID,'landmarkPos3D')
    p.landmarkLabels=hdfgetdata(gID,'landmarkLabels')
             
    
    return p

def read_aux(gID):
    a=aux
    a.name=hdfgetdata(gID,'name')
    a.dataTimeSeries=hdfgetdata(gID,'dataTimeSeries')
    a.time=hdfgetdata(gID,'time')
    a.timeOffSet=hdfgetdata(gID,'timeOffSet')
    
    return a

def read_stim(gID):    
    s=stim
    s.name=hdfgetdata(gID,'name')
    s.data=hdfgetdata(gID,'data')   
    return s        
         
         
def read_measurementList(gID):
    m=measurementList
    
    
    
    m.sourceIndex=hdfgetdata(gID,'sourceIndex')
    m.detectorIndex=hdfgetdata(gID,'detectorIndex')
    m.wavelengthIndex=hdfgetdata(gID,'wavelengthIndex')
    m.wavelengthActual=hdfgetdata(gID,'wavelengthActual')
    m.wavelengthEmissionsActual=hdfgetdata(gID,'wavelengthEmissionsActual')
    m.dataType=hdfgetdata(gID,'dataType')
    m.dataTypeLabel=hdfgetdata(gID,'dataTypeLabel')
    m.dataTypeIndex=hdfgetdata(gID,'dataTypeIndex')
    m.sourcePower=hdfgetdata(gID,'sourcePower')
    m.detectorGain=hdfgetdata(gID,'detectorGain')
    m.moduleIndex=hdfgetdata(gID,'moduleIndex')
    
    return m

    
def hdfgetdata(gID,field):
        val = gID.get(field)
        if val is None:
            return val
        
        if h5py.check_string_dtype(val.dtype):
            # string
            if val.len()==1:
                val=val[0].tostring().decode('ascii')
                return val
            else:
                val2=[];
                for x in val:
                    val2.append(x.tostring().decode('ascii'))
                val2=np.array(val2)
                return val2
        val=np.array(val)
        
        if(val.ndim==1 and len(val)==1):
            val=val[0]    
        
        return val



def getrequiredfieldsLst():
     Required=[];
     Required.append("/formatVersion")
     Required.append("/nirs\d*/data\d*/dataTimeSeries")
     Required.append("/nirs\d*/data\d*/time")
     Required.append("/nirs\d*/data\d*/measurementList\d*/sourceIndex")
     Required.append("/nirs\d*/data\d*/measurementList\d*/detectorIndex")
     Required.append("/nirs\d*/data\d*/measurementList\d*/wavelengthIndex")
     Required.append("/nirs\d*/data\d*/measurementList\d*/dataType")
     Required.append("/nirs\d*/data\d*/measurementList\d*/dataTypeIndex")       
     Required.append("/nirs\d*/probe/sourcePos\d*")
     Required.append("/nirs\d*/probe/detectorPos\d*")
     return Required        
            
def getoptionalfieldsLst():
     Optional=[]
     Optional.append("/nirs\d*/metaDataTags/\w*")
     Optional.append("/nirs\d*/data\w*/measurementList\d*/sourcePower")
     Optional.append("/nirs\d*/data\w*/measurementList\d*/detectorGain")
     Optional.append("/nirs\d*/data\w*/measurementList\d*/moduleIndex")
     Optional.append("/nirs\d*/data\d*/measurementList\d*/dataTypeLabel")
     Optional.append("/nirs\d*/stim\w*/name")
     Optional.append("/nirs\d*/stim\w*/data")
     Optional.append("/nirs\d*/probe/wavelengths")
     Optional.append("/nirs\d*/aux\d*/name")
     Optional.append("/nirs\d*/aux\d*/dataTimeSeries")
     Optional.append("/nirs\d*/aux\d*/time")
     Optional.append("/nirs\d*/aux\d*/timeOffset")
     Optional.append("/nirs\d*/probe/wavelengthsEmission")
     Optional.append("/nirs\d*/probe/sourcePos2D")
     Optional.append("/nirs\d*/probe/sourcePos3D")
     Optional.append("/nirs\d*/probe/detectorPos2D")
     Optional.append("/nirs\d*/probe/detectorPos3D")
     Optional.append("/nirs\d*/probe/frequencies")
     Optional.append("/nirs\d*/probe/timeDelays")
     Optional.append("/nirs\d*/probe/timeDelayWidths")
     Optional.append("/nirs\d*/probe/momentOrders")
     Optional.append("/nirs\d*/probe/correlationTimeDelays")
     Optional.append("/nirs\d*/probe/correlationTimeDelayWidths")
     Optional.append("/nirs\d*/probe/sourceLabels")
     Optional.append("/nirs\d*/probe/detectorLabels")
     Optional.append("/nirs\d*/probe/landmarkPos2D")
     Optional.append("/nirs\d*/probe/landmarkPos")
     Optional.append("/nirs\d*/probe/landmarkPos3D")
     Optional.append("/nirs\d*/probe/landmarkLabels")
     Optional.append("/nirs\d*/probe/useLocalIndex")
    
     return Optional


def isrequired(fld):
    flag = False
    required=getrequiredfieldsLst()
    for x in required:
        if re.match(x,fld):
            flag = True
    return flag


def isoptional(fld):
    flag = False
    required=getoptionalfieldsLst()
    for x in required:
        if re.match(x,fld):
            flag = True
    return flag


        
        


def validate(filename,fileOut=None):
     fileID = h5py.File(filename, 'r')
     formatVersion=hdfgetdata(fileID,"/formatVersion")
  
     def getallnames(gID,lst):
         if isinstance(gID, h5py.Dataset):  
             lst.append(gID.name)
         else:
            for x in gID:
                getallnames(gID[x],lst)
                
     def checkdim(field,fID,foundInvalid,lstInvalid):
         val = fID.get(field);
    
         if "Pos2D" in field:
             dim = 2;
         elif "Pos3D" in field:
             dim = 2;
         elif "dataTimeSeries"in field and "aux" in field:
             dim = 1;
         elif "dataTimeSeries" in field:
             dim = 2;
         elif  ("stim" in field)and ("data" in field):
             dim = 2;
         else:
             dim = 1;
         if dim != len(val.dims):
             return False
    
     lst=[]  
    
     getallnames(fileID,lst)
     
     
     
     if fileOut == None:
         print('-' * 40)
         print('SNIRF Validator')
         print('Version 1.0')
         print('written by T. Huppert')
         print()
         print('File = {0}'.format(filename))   
         print('Version = {0}'.format(formatVersion))
         print('-' * 40)
          
         foundInvalid=0;
        
         lstInvalid=[]
        
         for x in lst:
            print(Fore.WHITE + x)
            val = fileID.get(x)
            if h5py.check_string_dtype(val.dtype):
                # string
                if val.len()==1:
                    val=val[0].tostring().decode('ascii')
                    print('\tHDF5-STRING: {0}'.format(val))
                else:
                    val2=[];
                    for y in val:
                        val2.append(y.tostring().decode('ascii'))
                    val2=np.array(val2)
                    print('\tHDF5-STRING 1D-Vector: <{0}x1>'.format(len(val2)))
            else:
                val=np.array(val)
                if(val.ndim==1 and len(val)==1):
                    val=val[0]    
                    print('\tHDF5-FLOAT: {0}'.format(val))
                elif val.ndim==1:
                    
                     print('\tHDF5-FLOAT 1D-Vector: <{0}x1>'.format(len(val)))
                else:
                     print('\tHDF5-FLOAT 2D-Array: <{0}x{1}>'.format(len(val),int(val.size/len(val))))
                
            dimcheck = checkdim(x, fileID, foundInvalid, lstInvalid)
            if dimcheck == False:
                val = len(fileID.get(x).dims)
                if val == 1:
                    print(Fore.RED +'\tINVALID dimensions(Expected Number of Dimensions: 2)')
                else:
                    print(Fore.RED +'\tINVALID dimensions(Expected Number of Dimensions: 1)')
                foundInvalid=foundInvalid+1;
                lstInvalid.append(x)


            if isrequired(x)==True:
                print(Fore.BLUE + '\t\tRequired field')
            elif isoptional(x):
                print(Fore.GREEN +'\t\tOptional field')
            else:
                print(Fore.RED +'\t\tINVALID field')
                foundInvalid=foundInvalid+1
                lstInvalid.append(x)
        
         print('-' * 40)
         if(len(lstInvalid)!=0):
              print(Fore.RED+ "File is INVALID")
              print(Fore.RED +'\tINVALID ENTRIES FOUND')
              for x in lstInvalid:
                  print(Fore.RED + x)
         else:
              print(Fore.WHITE+ "File is VALID")
         print(Style.RESET_ALL)
     else: # write to file
         text_file = open(fileOut, "w")
         text_file.write('\n' + '\n' + '-' * 40)
         text_file.write('\n' + '\n' + 'SNIRF Validator')
         text_file.write('\n' + '\n' + 'Version 1.0')
         text_file.write('\n' + 'written by T. Huppert')
         text_file.write('\n')
         text_file.write('\n' + 'File = {0}'.format(filename))   
         text_file.write('\n' + 'Version = {0}'.format(formatVersion))
         text_file.write('\n' + '-' * 40)
          
         foundInvalid=0;
        
         lstInvalid=[]
        
         for x in lst:
            text_file.write('\n' + x)
            val = fileID.get(x)
            if h5py.check_string_dtype(val.dtype):
                # string
                if val.len()==1:
                    val=val[0].tostring().decode('ascii')
                    text_file.write('\n' + '\tHDF5-STRING: {0}'.format(val))
                else:
                    val2=[];
                    for y in val:
                        val2.append(y.tostring().decode('ascii'))
                    val2=np.array(val2)
                    text_file.write('\n' + '\tHDF5-STRING 1D-Vector: <{0}x1>'.format(len(val2)))
            else:
                val=np.array(val)
                if(val.ndim==1 and len(val)==1):
                    val=val[0]    
                    text_file.write('\n' + '\tHDF5-FLOAT: {0}'.format(val))
                elif val.ndim==1:
                    
                     text_file.write('\n' + '\tHDF5-FLOAT 1D-Vector: <{0}x1>'.format(len(val)))
                else:
                     text_file.write('\n' + '\tHDF5-FLOAT 2D-Array: <{0}x{1}>'.format(len(val),int(val.size/len(val))))
                
            dimcheck = checkdim(x, fileID, foundInvalid, lstInvalid)
            if dimcheck == False:
                val = len(fileID.get(x).dims)
                if val == 1:
                    text_file.write(Fore.RED +'\tINVALID dimensions(Expected Number of Dimensions: 2)')
                else:
                    text_file.write(Fore.RED +'\tINVALID dimensions(Expected Number of Dimensions: 1)')
                foundInvalid=foundInvalid+1
                lstInvalid.append(x)
            
            if isrequired(x)==True:
                text_file.write('\n' + '\t\tRequired field')
            elif isoptional(x):
                text_file.write('\n' + '\t\tOptional field')
            else:
                text_file.write('\n' + '\t\tINVALID field')
                foundInvalid=foundInvalid+1
                lstInvalid.append(x)
        
         text_file.write('\n' + '-' * 40)
         if(len(lstInvalid)!=0):
              text_file.write('\n' + "File is INVALID")
              text_file.write('\n' + '\tINVALID ENTRIES FOUND')
              for x in lstInvalid:
                  text_file.write('\n' +  x)
         else:
              text_file.write('\n' + "File is VALID")
         text_file.close()
              
     return (foundInvalid==0)
    
 
def main():
    
    filename=sys.argv[1]
    print(filename)
    if(len(sys.argv)>2):
        fileOut=sys.argv[2]
    else:
        fileOut=None
    validate(filename,fileOut)
    
if __name__ == "__main__":
    main()
    
    
    
