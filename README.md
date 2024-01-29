## TFG - Prompt sentiment
![Prompt sentiment](https://github.com/tgs1003/TFG_2023_2024/blob/main/Documentaci%C3%B3n/Manual%20de%20usuario/img/Logo2.png?raw=true)

## Autor
- Teodoro Ricardo García Sánchez

## Tutores
- Virginia Ahedo García
- Jose Ignacio Santos Martín

### Resumen
Las reseñas ofrecen una valiosa información sobre la percepción de los usuarios respecto a productos y servicios. 

Por ello, se ha desarrollado una aplicación que utiliza un **LLM** (mediante *prompts*) para el análisis, clasificación y calificación de reseñas de usuarios.

Utilizamos el conocimiento de estos modelos preentrenados para diseñar e implementar de forma ágil una solución a este problema.

### Página web

https://promptsentiment.es

### Videos
#### Presentación

#### Demostración


### Instalación con docker

#### Instalar Docker Desktop

https://docs.docker.com/engine/install/

#### Clonar repositorio:

`git clone https://github.com/tgs1003/TFG_2023_2024.git
`

#### Cambiar al directorio donde está el código:
`Code/prompt_sentiment`


#### Modificar el fichero docker-compose.yml para incluir la API key (`OPENAI_API_KEY`) de OpenAI.

https://platform.openai.com/api-keys

#### Alternativamente se puede configurar para usar la api de hugging face (`HUGGINGFACE_API_KEY`):

https://huggingface.co/settings/tokens

En este caso, hay que cambiar el valor de LLM_API a OpenChat.

#### Ejecutar
```
docker-compose up
```

Para acceder a la aplicación, abrir desde cualquier explorador:
```
http://localhost:8080
```
El administrador por defecto es:
```
Usuario: admin@promptsentiment.es

Contraseña: ubu_1234
```

### Calidad de código
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e78f97bd472241a79ef97cae0de00de7)](https://app.codacy.com/gh/tgs1003/TFG_2023_2024/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
### Gestión del proyecto

https://zube.io/tgs1003/tfg_2023_2024


