@echo off
echo 请使用ANSI编码
%echo 若提示找不到文件，请编辑LRWaterMark_semi-utils.bat以修改其指向的目录
cd %~dp0
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEG" --output_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEGwithWaterMark"
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\Cache" --output_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\CachewithWaterMark"
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEGAAA" --output_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEGAAAwithWaterMark"
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEG" --output_dir "D:\00-OnedriveRoot\001-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEGAAAwithWaterMark-wechat" --resolution 2155 --quality 90 --shape 2.1 --file_younger_than 7 --force_y_padding True
python "main.py" -c config.yaml --input_dir "D:\Adobe_Cache\HXX" --output_dir "D:\01_Backups\RMN10Pro\徐定民\00Files\xiaxia"
python "main.py" -c config.yaml --input_dir "D:\Adobe_Cache\Clear-All-Info\JPEG" --output_dir "D:\Adobe_Cache\Clear-All-Info\JPEG_Clear" --incognito_remove_all_exif_iptc True
pause