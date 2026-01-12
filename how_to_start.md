## visual Studio Code

## how to start FinancialPlanner
0. idz do C:\Users\user\source\repos\P_WebApp
1. env/Scripts/activate (wazne! tutaj jest katalog env!)
2. idz do C:\Users\user\source\repos\P_WebApp\SwsApp
3. python manage.py runserver

## start fast api
0. idz do C:\Users\user\source\repos\P_FastApi
1.python ./accesstoPlannerDb.py
2. go http://127.0.0.1:8000/


# tests
0. idz do C:\Users\user\source\repos\P_WebApp
1. env/Scripts/activate (wazne! tutaj jest katalog env!)
2. idz do C:\Users\user\source\repos\P_WebApp\FamilyActivity
3. python manage.py test
4. Jesli sa testy to je znajdzie i odpali
5. przykladowe testy sa tutaj ./ActivityDay


## how to start swsdb app (obie applikacje musz byc aktywne fast api i django projekt)
0. idz do C:\Users\user\source\repos\P_FastApi
1. odpal w vsc plik accesstoSwsDb.py
2. idz do C:\Users\user\source\repos\P_WebApp
3. env/Scripts/activate (wazne! tutaj jest katalog env!)
4. idz do C:\Users\user\source\repos\P_WebApp\SwsApp
5. python manage.py runserver i go http://127.0.0.1:8000/

## mozna startowac przy uzyciu SWS_start.bat and go http://127.0.0.1:8000/
1. idz do idz do C:\Users\user\source\repos\P_FastApi
2. sa tu pliki bat
 ale to nie do konca dobrze dziala.
 SWE_Stop.bat nie do konca kiluje.