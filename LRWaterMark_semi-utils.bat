@echo off
echo ��ʹ��ANSI����
%echo ����ʾ�Ҳ����ļ�����༭LRWaterMark_semi-utils.bat���޸���ָ���Ŀ¼
cd %~dp0
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\002-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEG" --output_dir "D:/00-OnedriveRoot/002-mail.sdu.edu.cn/OneDrive - mail.sdu.edu.cn/LightroomOutput/JPEGwithWaterMark"
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\002-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEGAAA" --output_dir "D:/00-OnedriveRoot/002-mail.sdu.edu.cn/OneDrive - mail.sdu.edu.cn/LightroomOutput/JPEGAAAwithWaterMark"
python "main.py" -c config.yaml --input_dir "D:\00-OnedriveRoot\002-mail.sdu.edu.cn\OneDrive - mail.sdu.edu.cn\LightroomOutput\JPEG" --output_dir "D:/00-OnedriveRoot/002-mail.sdu.edu.cn/OneDrive - mail.sdu.edu.cn/LightroomOutput/JPEGAAAwithWaterMark-wechat" -r 2155 -q 90 -s 2.1 -y 7
pause