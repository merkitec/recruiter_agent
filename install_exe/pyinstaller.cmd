pyinstaller --noconfirm --add-data "C:\Users\ytamayo\AppData\Local\Temp\.seleniumwire\ca.crt;./seleniumwire/" --add-data "C:\Users\ytamayo\AppData\Local\Temp\.seleniumwire\ca.key;./seleniumwire/" --add-data "C:\Apps\Anaconda3\envs\recruiter_agent\Lib\site-packages\pypdfium2_raw\pdfium.dll;./pypdfium2_raw/" --add-data "C:\Apps\Anaconda3\envs\recruiter_agent\Lib\site-packages\pypdfium2_raw\version.json;./pypdfium2_raw/" --add-data "C:\Apps\Anaconda3\envs\recruiter_agent\Lib\site-packages\pypdfium2\\version.json;./pypdfium2/" --onefile --console  --paths=C:\Apps\Anaconda3\envs\recruiter_agent\Lib main.py