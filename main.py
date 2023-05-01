import math
import os
import time

import yaml
#import piexif
import pyexiv2
from PIL import Image, ImageDraw
from PIL import ImageFont
from PIL.Image import Transpose


from utils import parse_datetime, get_file_list, concat_img, get_exif, get_str_from_exif

# 布局，全局配置
FONT_SIZE = 240
BORDER_PIXEL = 60
UP_DOWN_MARGIN = FONT_SIZE + BORDER_PIXEL
LEFT_RIGHT_MARGIN = FONT_SIZE + BORDER_PIXEL
GAP_PIXEL = 90

# 读取配置
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 读取输入、输出配置
input_dir = config['base']['input_dir']
output_dir = config['base']['output_dir']
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
quality = config['base']['quality']

# 读取字体配置
font = ImageFont.truetype(config['base']['font'], FONT_SIZE)
bold_font = ImageFont.truetype(config['base']['bold_font'], FONT_SIZE)

# 读取 logo 配置
logo_enable = config['logo']['enable']
makes = config['logo']['makes']

# 读取等效焦距配置
# 先将像素密度铺满135画幅，之后通过分辨率计算出等效焦距。优点是能考虑裁切的影响

full_fram_resolutions=[]
if config['equivalent_focal_length']['enable']:
    for cameraname in config['equivalent_focal_length']:
        if cameraname != 'enable':
            crop=config['equivalent_focal_length'][cameraname][2]['crop']
            x=config['equivalent_focal_length'][cameraname][0]['sensor_resolution_X']
            y=config['equivalent_focal_length'][cameraname][1]['sensor_resolution_Y']
            multi_sensor=config['equivalent_focal_length'][cameraname][3]['multi_sensor']
            rename=config['equivalent_focal_length'][cameraname][4]['rename']
            full_fram_resolutions.append((cameraname,x*crop,y*crop,multi_sensor,rename))
full_fram_resolutions=tuple(full_fram_resolutions)
print('Load camera resolutions')
print(full_fram_resolutions)            

# 添加 logo
def append_logo(exif_img, exif):
    logo = None
    if 'Make' in exif:
        make = exif['Make']
        try:
            for m in makes.values():
                if m['id'] == make+'_'+exif['Artist']:
                        logo = Image.open(m['path'])
        except:
            pass
        if logo == None:
            
            for m in makes.values():
                if m['id'] in make:
                    logo = Image.open(m['path'])
    if logo is not None:
        logo = logo.resize((exif_img.height, exif_img.height), Image.Resampling.LANCZOS)
        exif_img.paste(logo, (0, 0))


def make_two_line_img(first, second):
    mask_first = bold_font.getmask(first)
    mask_second = font.getmask(second)
    m1_width = mask_first.size[0] if first != '' else bold_font.getmask('A').size[0]
    m2_width = mask_second.size[0] if second != '' else font.getmask('A').size[0]
    m1_height = mask_first.size[1] if first != '' else bold_font.getmask('A').size[1]
    m2_height = mask_second.size[1] if second != '' else font.getmask('A').size[1]
    _img = Image.new('RGB', (
        max(m1_width, m2_width), m1_height + m2_height + GAP_PIXEL * 3),
                     color='white')
    draw = ImageDraw.Draw(_img)
    draw.text((0, 0), first, font=bold_font, fill='black')
    draw.text((0, m1_height + GAP_PIXEL), second, font=font, fill='gray')
    return _img


def make_normal_watermark(exif, infos, filename):
    original_width, original_height = infos['original_width'], infos['original_height']
    all_ratio, font_ratio = infos['all_ratio'], infos['font_ratio']
    # 位置 1
    c_11 = get_str_from_exif(exif, elements[0], filename)
    c_12 = get_str_from_exif(exif, elements[1], filename)
    img_1 = make_two_line_img(c_11, c_12)

    # 位置 2
    c_21 = get_str_from_exif(exif, elements[2], filename)
    c_22 = get_str_from_exif(exif, elements[3], filename)
    img_2 = make_two_line_img(c_21, c_22)

    img_watermark = Image.new('RGB', (original_width, math.floor(all_ratio * original_width)), color='white')
    left_margin = BORDER_PIXEL
    right_margin = BORDER_PIXEL

    # 根据照片长缩放水印元素
    img_1_x_length = math.floor(img_1.width / img_1.height * math.floor(original_width * font_ratio))
    img_2_x_length = math.floor(img_2.width / img_2.height * math.floor(original_width * font_ratio))
    img_1_y_length = math.floor(original_width * font_ratio)
    img_2_y_length = math.floor(original_width * font_ratio)
    img_1 = img_1.resize((img_1_x_length, img_1_y_length), Image.Resampling.LANCZOS)
    img_2 = img_2.resize((img_2_x_length, img_2_y_length), Image.Resampling.LANCZOS)

    # 是否添加 logo
    if logo_enable:
        append_logo(img_watermark, exif)
        # 计算边界
        left_margin += img_watermark.height

    # 拼接元素 1 和元素 2
    img_watermark.paste(img_1, (left_margin, math.floor((all_ratio - font_ratio) / 2 * original_width)))
    img_watermark.paste(img_2, (
        img_watermark.width - img_2.width - right_margin, math.floor((all_ratio - font_ratio) / 2 * original_width)))

    return img_watermark


elements = config['layout']['elements']


# 生成元信息图片
def make_exif_img(exif, layout, filename):
    # 修改水印长宽比
    font_ratio = .07
    all_ratio = .13
    original_width = exif['ExifImageWidth']
    original_height = exif['ExifImageHeight']
    original_ratio = original_width / original_height
    if original_ratio > 1:
        font_ratio = .07
        all_ratio = .1

    wm_x_length = original_width
    wm_y_length = math.floor(all_ratio * original_width)
    img_watermark = Image.new('RGB', (wm_x_length, wm_y_length))
    settings = {'original_width': original_width, 'original_height': original_height, 'all_ratio': all_ratio,
                'font_ratio': font_ratio}
    if layout == 'normal':
        img_watermark = make_normal_watermark(exif, settings, filename)
    # 根据照片长缩放水印
    return img_watermark.resize((wm_x_length, wm_y_length), Image.Resampling.LANCZOS)

# 保存输入文件名及修改日期
def save_file_change_time(input_dir,document_change_time_list):
    file = open(os.path.join(input_dir, 'semi-utils_file_change_time_for.pylist'), 'w')
    for fp in document_change_time_list:
        file.write(str(fp))
        file.write('\n')
    file.close()

# 读取上次运行时已经处理过的文件信息
def read_file_change_time(input_dir):
    try:
        file = open(os.path.join(input_dir, 'semi-utils_file_change_time_for.pylist'), 'r')
        document_load = []
        for line in file.readlines():
            line = line.strip('\n')
            document_load.append(line)
        file.close()
    except:
        document_load=[]
    return document_load

if __name__ == '__main__':
    file_list = get_file_list(input_dir)
    layout = config['layout']['type']
    file_write=[]
    #file_skip=[]
    file_skip_count=0
    
    
    new_list_file_change_time=[]#新的列表，存放这次运行时输入文件的修改时间
    old_list_file_change_time=read_file_change_time(input_dir)#旧的列表，存放上一次运行时输入文件的修改时间
    
    for file in file_list:
        
        skip_this_file=False
        target=os.path.join(output_dir, file)
        source=os.path.join(input_dir, file)
        file_change_time=str(time.ctime(os.stat(source).st_mtime))
        new_list_file_change_time.append([file,file_change_time])
        
        
        if(os.path.exists(target)):
            #skip_this_file=True
            #跳过未修改的文件
            if str([file,file_change_time]) in old_list_file_change_time:
                skip_this_file = True
            else:
                skip_this_file = False
        
        
        
        if(skip_this_file == False ):
            # 打开图片
            img = Image.open(source)
            # 生成 exif 图片
            exif = get_exif(img,full_fram_resolutions,config,file)
            # 修复图片方向
            if 'Orientation' in exif:
                if exif['Orientation'] == 3:
                    img = img.transpose(Transpose.ROTATE_180)
                elif exif['Orientation'] == 6:
                    img = img.transpose(Transpose.ROTATE_270)
                elif exif['Orientation'] == 8:
                    img = img.transpose(Transpose.ROTATE_90)
            exif['ExifImageWidth'], exif['ExifImageHeight'] = img.width, img.height
            
            
            
            exif_img = make_exif_img(exif, layout, file)
            #print(file)
            # 拼接两张图片
            cnt_img = concat_img(img, exif_img)

            cnt_img.save(target, quality=quality )
            cnt_img.close()
            img.close()
            
            #拷贝EXIF和IPTC等元数据
            imgin_pyexiv2=pyexiv2.Image(source,encoding='GBK')
            imgtarget_pyexiv2=pyexiv2.Image(target,encoding='GBK')
            
            orgiptc=imgin_pyexiv2.read_iptc()
            orgxmp=imgin_pyexiv2.read_raw_xmp()
            orgexif=imgin_pyexiv2.read_exif()
            orgcomment=imgin_pyexiv2.read_comment()
            orgicc=imgin_pyexiv2.read_icc()
            orgthumbnail=imgin_pyexiv2.read_thumbnail()
            
            
            imgtarget_pyexiv2.modify_iptc(orgiptc)
            imgtarget_pyexiv2.modify_raw_xmp(orgxmp)
            imgtarget_pyexiv2.modify_exif(orgexif)
            #imgtarget_pyexiv2.modify_comment(orgcomment)
            #imgtarget_pyexiv2.modify_icc(orgicc)  
            #imgtarget_pyexiv2.modify_thumbnail(orgthumbnail)
            
            imgin_pyexiv2.close()
            imgtarget_pyexiv2.close()
            #print(img.info)
            #print(" WRITE "+target[-30:])
            file_write.append(" WRITE "+target[-30:])
            print(file_write[-1])
        else:
            pass
            file_skip_count=file_skip_count+1
            #file_skip.append("#SKIP# "+target[-30:])
            #print(file_skip[-1])
        
        
    print()
    print("SKIP  "+str(file_skip_count)+" Files")
    print("WRITE "+str(len(file_write))+" Files")
    save_file_change_time(input_dir,new_list_file_change_time)
    