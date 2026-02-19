## django project, nie dziala w termux
## visual Studio Code

## how to start swsdb app (obie applikacje musz byc aktywne fast api i django projekt)
0. idz do C:\Users\user\source\repos\P_SWSWebApp
1. env/Scripts/activate (wazne! tutaj jest katalog env!)
2. python manage.py runserver i go http://127.0.0.1:8000/

## fast api
3. C:\Users\user\source\repos\P_AppMobile\P_SWS
4. uvicorn main:app --host 0.0.0.0 --port 8001 --reload 
