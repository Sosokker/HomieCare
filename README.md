# HomieCare

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Reference](#Reference)

## Installation

First of all clone this repository then install requirement file in `requirements\base.txt`

Recommend to create virtual environment

### Podman Container

First of all, you need podman (it's like a docker but daemonless)

[Podman installation](https://podman.io/docs/installation)

#### Install MinIO

You can follow detailed step [here](https://min.io/download)

**Window**

```bash
podman run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"
```

#### Install PhpmyAdmin and MySQL

```bash
# Pull mysql and phpmyadmin then create network
podman pull docker.io/library/mysql docker.io/library/phpmyadmin
podman network create net-pma

# Run both Images
podman run --name service-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root --network net-pma -d docker.io/library/mysql

podman run --name service-pma -p 8080:80 -e PMA_HOST=service-mysql --network net-pma -d docker.io/library/phpmyadmin
```

### Download Model files then put in project

[Download here](https://drive.google.com/drive/folders/1GGcKz8bqPll6PWNh4bPjFIH0fmOdof4p?usp=sharing)
[Download data to import to sql here](https://drive.google.com/drive/folders/15hmaJOK1-Xj1cMdl8Ajss_UuBf-vKqxr?usp=sharing)

Then put into following path (Not fix to be this path but it would be great)

- sppe, TSSTG, yolo-tiny-onecls folder -> `StreamServer\src\analytic\action\Models`

- xgboost_model.pkl -> `StreamServer\src\analytic\health`

### Create .env file

Take a look at description in example.env and fill out those parameter

### Install node dependencies

```
cd frontend
pnpm
```

## Usage

### Start Server

Start server with main.py in `StreamServer\src`

```bash
py main.py
```

### Run React

Start server with this command in `frontend`

```bash
pnpm dev
```

Then access webpage at [http://localhost:5173/](http://localhost:5173/)

Visit API documentation at [http://127.0.0.1:8000/api/v1/docs/swagger/](http://127.0.0.1:8000/api/v1/docs/swagger/) or
[http://127.0.0.1:8000/api/v1/docs/](http://127.0.0.1:8000/api/v1/docs/)

## Reference

- [Human-Falling-Detect-Tracks by GajuuzZ](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks)
- [TailAdmin](https://tailadmin.com/)
