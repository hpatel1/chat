# chat
Chat appliatino using python django with real time notification using channels


>pip install -r requirement.txt

##Dependecy downloads
>apt install libffi-dev
>apt install redis-server
>service redis-server restart

##Run server
>python manage.py runserver

Hit http://localhost:8000 in Chrome browser. It will connect channel chat-hardik with server

open debugger tool (F12) in Chrome, to see the notification.
To see notification, login to admin section and create message object by other than hpatel@vavni.com user.
