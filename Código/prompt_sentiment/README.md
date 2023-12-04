Para la base de datos se ha usado Docker:
https://www.docker.com/get-started/

Este comando instancia una base de datos postgres en la máquina local usando el puerto 5432.

La contraseña del usuario "postgres" es "postgres".
docker run -itd -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v -d postgres