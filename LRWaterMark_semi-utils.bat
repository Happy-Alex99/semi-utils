@echo off
echo 请使用ANSI编码
%echo 若提示找不到文件，请编辑LRWaterMark_semi-utils.bat以修改其指向的目录
cd %~dp0
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\002-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEG" --output_dir "D:/00-OnedriveRoot/002-mail.sdu.edu.cn/OneDrive - mail.sdu.edu.cn/LightroomOutput/JPEGwithWaterMark"
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\002-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEGAAA" --output_dir "D:/00-OnedriveRoot/002-mail.sdu.edu.cn/OneDrive - mail.sdu.edu.cn/LightroomOutput/JPEGAAAwithWaterMark"
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\002-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEGAAA" --output_dir "D:/00-OnedriveRoot/002-mail.sdu.edu.cn/OneDrive - mail.sdu.edu.cn/LightroomOutput/JPEGAAAwithWaterMark-1080p" -r 1080 -q 100
pause