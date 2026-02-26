=====EJECUCION=======  
1. Llenar .env copiando de .env.example  
2. Ejecutar con docker  
$ docker compose up -d  
3. Probar POST en http://127.0.0.1:8000/chat  
  
=====EJECUCION LOCAL MODO DEV=====  
Preparacion  
1. Crear venv y activarlo  
$ python -m venv venv  
$ ./venv/Scripts/activate  
  
2. Instalar dependencias  
$ pip install -r requirements.txt   
  
3. Para probar el agente  
$ python -m agent.agent  
  
4. Para ejecutar la api en modo debug  
$ fastapi dev  
  
5. Probar POST en http://127.0.0.1:8000/chat  