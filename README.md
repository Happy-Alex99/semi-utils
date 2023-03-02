
# semi-utils
一个批量添加相机机型和拍摄参数的工具，后续「可能」添加其他功能。



## 功能列表

- [x] 支持显示厂商 logo
- [x] 支持显示相机机型和厂商名
- [x] 支持显示拍摄参数（焦距、光圈、快门速度）
- [x] 支持显示等效焦距
- [x] 支持复制 exif 信息到输出的文件中
- [x] 支持Lightroom导出后自动拉起脚本
- [x] 跳过上一次运行时已经处理的文件，但源文件有新修改时除外


## 配置项

| 参数                                            | 描述                                                                         |
| ----------------------------------------------- | --------------------------------------------------------------------------   |
| base.font                                       | 水印字体路径，常规字重                                                       |
| base.bold_font                                  | 水印字体路径，加粗字重                                                       |
| base.input_dir                                  | 输入的原始照片，建议将原始照片复制一份到该文件夹                             |
| base.output_dir                                 | 输出的带水印的照片                                                           |
| base.quality                                    | 输出质量，默认为 100，可以输入 60-100 之间的数字                             |
| logo.enable                                     | true 或者 false，是否显示厂商 logo                                           |
| logo.makes                                      | 厂商 logo 列表，默认支持尼康、佳能、索尼、宾得，可自行添加配置               |
| logo.makes.item                                 | 厂商配置，一个带有 `id` 和 `path` 两个键的字典                               |
| logo.makes.item.id                              | 厂商标识，由 Exif 信息提供                                                   |
| logo.makes.item.path                            | 厂商 logo 路径，可自定义                                                     |
| equivalent_focal_length.enable                  | 等效焦距设置，启用                                                           |
| equivalent_focal_length.sensor_resolution_X     | 输入相机传感器的长边分辨率                                                   |
| equivalent_focal_length.sensor_resolution_Y     | 输入相机传感器的短边分辨率                                                   |
| equivalent_focal_length.crop                    | 输入相机传感器的135画幅裁切系数，如佳能APSC为1.6，其他APSC为1.5              |
