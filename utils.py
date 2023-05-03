# -*- encoding:utf-8 -*-
# 修改日期格式
import os
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS

import json

import pyexiv2
import re
def parse_datetime(datetime_string):
    return datetime.strptime(datetime_string, '%Y:%m:%d %H:%M:%S')


def get_file_list(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'jpg' in file or 'jpeg' in file or 'JPG' in file or 'JPEG' in file:
                file_list.append(file)
    return file_list


def concat_img(img_x, img_y):
    img = Image.new('RGB', (img_x.width, img_x.height + img_y.height), color='white')
    img.paste(img_x, (0, 0))
    img.paste(img_y, (0, img_x.height))
    return img


# 读取 exif 信息，包括相机机型、相机品牌、图片尺寸、镜头焦距、光圈大小、曝光时间、ISO 和拍摄时间
def get_exif(image,full_fram_resolutions,config,file):
    
    _exif = {}
    info = image._getexif()
    if info:
        try:
            _exif['equivalent_focal_length']=0
            for attr, value in info.items():
                decoded_attr = TAGS.get(attr, attr)
                _exif[decoded_attr] = value
            _exif['Model']=_exif['Model'].split('\x00')[0]
            #计算等效焦距
        
            digital_zoom=1.0
            for full_fram_resolution in full_fram_resolutions:
                if full_fram_resolution[0]==_exif['Model']:
                    if full_fram_resolution[3]==1:#only 1 sensor
                        full_fram_resolutionX=full_fram_resolution[1]
                        full_fram_resolutionY=full_fram_resolution[2]
                    else:
                        #camera or mobile phone with more than 1 camera
                        multi_sensor=[]
                        #read multi sensor information directly from config
                        for item in config['equivalent_focal_length'][_exif['Model']]:
                            for key in item:
                                multi_sensor.append(item[key])
                        
                        #sensor information list as: FocalLength,full_fram_resolutionX,full_fram_resolutionY. Will NOT check the order
                        sensor_index=multi_sensor.index(str(_exif['FocalLength'])+'mm')
                        
                        full_fram_resolutionX=multi_sensor[sensor_index+1]
                        full_fram_resolutionY=multi_sensor[sensor_index+2]
                        
                        try:
                            digital_zoom=digital_zoom*json.loads(_exif[39321])['ZoomMultiple']#Xiaomi Redmi Note 10 Pro
                        except:
                            pass
                        try:
                            digital_zoom=(digital_zoom*_exif['DigitalZoomRatio'])/100
                        except:
                            pass
                    
                    break
            
            _exif['Model']=full_fram_resolution[4]# Rename camera name
            try:
                _exif['LensModel']=config['lens_rename'][_exif['LensModel']][0]['rename']#rename lens
            except:
                pass
            print(_exif['LensModel'])
            if 1:
                if image.size[0]>image.size[1]:
                    imageX=image.size[0]
                    imageY=image.size[1]
                else:
                    imageX=image.size[1]
                    imageY=image.size[0]
                
                
               
                tmp1=full_fram_resolutionX/imageX
                tmp2=full_fram_resolutionY/imageY
                tmp3=_exif['FocalLength']*tmp1 if tmp1<tmp2 else _exif['FocalLength']*tmp2
                _exif['equivalent_focal_length']=tmp3*digital_zoom
                #print(_exif)
                #print(digital_zoom)
        except:
            pass #_exif['equivalent_focal_length']=int(_exif['equivalent_focal_length'])
    if 'PANO' in file.upper():
        _exif['equivalent_focal_length']='PANO'
    if 'MERGE' in file.upper():
        _exif['equivalent_focal_length']='MERGE'
    if 'MULTI' in file.upper():
        _exif['equivalent_focal_length']='MULTI'
    #print(_exif)
    return _exif

ExposureProgram_str=['?','M','Auto','Av','Tv','DoF','Speed','Bof','Bif']
def ExposureProgram_2_str(ExposureProgram):
    try:
        return ExposureProgram_str[ExposureProgram]
    except:
        print('unknow ExposureProgram')
        return '??'

def get_filename_number(filename):
    #return filename.split('.')[0][-4:]
    #filename.split('-')[1].split('_')[1][:4]
    numbers_4_in_filename=re.findall('\d{4,}',filename)
    try:
        return numbers_4_in_filename[1]
    except:
        print('cannot obtain file number')
        return '    '

def ExposureBias2str (ev, force_plus_when0=0, end_with_Ev=1):#
    _ev=int(float(ev)*10)/10
    if _ev > 0:
        ev_str = '+'+str(_ev)+''
    elif _ev == 0:
        if force_plus:
            ev_str = '+0'
        else:
            ev_str = '0'
    else:
        ev_str = str(_ev)
    if end_with_Ev:
        ev_str=ev_str+'Ev'
    return ev_str

def ExposureBias2str_dual (ev_shoot, ev_lightroom):
    
    return ExposureBias2str(ev_shoot,end_with_Ev=0)+ExposureBias2str(ev_shoot, force_plus_when0=1,end_with_Ev=1)
    
    
        
def get_str_from_exif(exif, field, filename, xmp):
    if 'id' not in field:
        return ''
    field_id = field.get('id')
    if 'Param' == field_id:
        return get_param_str_from_exif(exif)
    elif 'Date' == field_id:
        try:
            return datetime.strftime(parse_datetime(exif['DateTimeOriginal']), '%Y-%m-%d %H:%M')
        except:
            return ""
    elif 'DateFilename' == field_id:
        try:
            
            return datetime.strftime(parse_datetime(exif['DateTimeOriginal']), '%Y-%m-%d %H:%M')+'  ['+get_filename_number(filename)+']'
        except:
            return ""
    elif 'Model_Exposureinfo' == field_id:
        try:
            ((int(float(xmp['Xmp.crs.Exposure2012'])*10))/10)
            exif_ExposureBiasValue=exif['ExposureBiasValue']
            xmp_ExposureBiasValue=xmp['Xmp.crs.Exposure2012']
            ExposureBiasValue_str=ExposureBias2str_dual(exif_ExposureBiasValue,xmp_ExposureBiasValue)
            
            #print(ExposureBiasValue_str)
            
            return '  '.join( (exif['Model'],ExposureProgram_2_str(exif['ExposureProgram']), ExposureBiasValue_str) )
        except:
            return ""
        
    else:
        if field_id in exif:
            return exif[field_id]
        else:
            return ''


def get_param_str_from_exif(exif):
    #print(exif)
    try:
        if exif['equivalent_focal_length']=='PANO' or exif['equivalent_focal_length']=='MERGE'or exif['equivalent_focal_length']=='MULTI':
            focal_length = str(int(exif['FocalLength'])) + '('+exif['equivalent_focal_length']+ ')' 'mm'
        else:
            if int(exif['equivalent_focal_length']):
                focal_length = str(int(exif['FocalLength'])) + '('+str(int(exif['equivalent_focal_length'])) + ')' 'mm'
            else:
                focal_length = str(int(exif['FocalLength'])) + 'mm'
        #print(focal_length)
    except:
        focal_length = ""
    try:
        f_number = 'F' + str(exif['FNumber'])
    except:
        f_number = ""
    try:
        exposure_time = str(exif['ExposureTime'].real)
    except:
        exposure_time = ""
    try:
        iso = 'ISO' + str(exif['ISOSpeedRatings'])
    except:
        iso = ""
    
    try:
        flash=''
        if int(exif['Flash'])&1: #Flash fired
            flash='FL'#chr(9889)#⚡
    except:
            flash=''
    
    return '  '.join((focal_length, f_number, exposure_time, iso, flash))
