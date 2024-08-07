from fastapi import FastAPI
import os
import configparser


# BASE FAST API SETTINGS

# создание приложения fast api и его общая настройка
root_path = os.environ.get("url_path") if os.environ.get("url_path") else '/no/path/specified'
IS_PRODUCTION = os.environ.get("PRODUCTION")
if IS_PRODUCTION:
    app = FastAPI(root_path=root_path, docs_url=None, redoc_url=None)
else:
    app = FastAPI(root_path=root_path)


# LOAD LOG CONFIG

# Чтение файла log.ini и замена его ENV переменныеми
config = configparser.ConfigParser()
config.read('log.ini')
log_filename = os.getenv('log_filename')
config.set('handler_logfile', 'args', f'''('/var/log/service-logs/{log_filename}','a')''')
with open('log_parsed.ini', 'w') as configfile:
    config.write(configfile)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", log_config="log_parsed.ini",
        host="0.0.0.0", port=80, reload=True)
