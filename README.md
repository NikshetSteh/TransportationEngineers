# Runing

1. Start docker engine (open Docker Desktop)
2. Go to project root
3. Use this command:
```shell
docker compose up --build
```

# Using

## Add test data

For adding test data you can use DebugConsole

> _**WARMING!!!**_
> First starting of face_server can be very slow, because it required to download and load model. Please, wait.

## Using Robot
For try robot function, use this step-by-step instruction:
1. Create engineer account using debug console
2. Provide privileges for engineer to auth robots
3. Run robot main file
4. Select state that you want to try

## Run any projects using poetry
1. Install dependencies:
```shell
poetry install
```
2. Activate environment:
```shell
poetry shell
```
3. Run project:
```shell
cd src
python main.py
```
or 
```shell
cd app
python main.py
```