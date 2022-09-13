import docker 
import sqlite3

def get_docker_client():
    return docker.from_env()


def get_app_ddl(app_image: str) -> str:
    """
    Return the ddl of the app
    """
    # create a docker client
    client = get_docker_client()
    # create a container from the app_image
    logs = client.containers.run(app_image, 'schema', auto_remove=True)
    # read the output of the container
    ddl = logs.decode('utf-8')
    # remove the container
    return ddl


def get_app_config_spec(app_image: str) -> str:
    """
    Return the configuration spec of the app
    """
    # create a docker client
    client = get_docker_client()
    # create a container from the app_image
    logs = client.containers.run(app_image, 'spec', auto_remove=True)
    # read the output of the container
    spec = logs.decode('utf-8')
    # remove the container
    return spec


def run_app_image(app_image, input_db_path, config_path, log_path):
    """
    Run the app image
    """
    # create a docker client
    client = get_docker_client()
    # mount the input_db_path and config_path to the container
    volumes = {
        input_db_path: {
            'bind': '/input.db',
            'mode': 'ro'
        },
        # mount as a file
        config_path: {
            'bind': '/config.json',
            'mode': 'ro'
        }
    }

    command = "run --input-db-path /input.db --config /config.json"

    # create a container from the app_image and mount the volumes
    container = client.containers.run(app_image, command, volumes=volumes, auto_remove=True, detach=True, )
    # redirect the output of the container to log_path
    with open(log_path, 'w') as f:
        for line in container.logs(stream=True):
            f.write(line.decode('utf-8'))



def verify_if_docker_image_exists(image_name: str) -> bool:
    """
    Return True if the docker image exists
    """
    client = get_docker_client()
    try:
        client.images.get(image_name)
        return True
    except docker.errors.ImageNotFound:
        return False

def setup_temp_db(db_path, app_image):
    """
    Create tables in db_path according to the DDL as specified by app_image
    """
    ddl = get_app_ddl(app_image)
    conn = sqlite3.connect(db_path)
    conn.executescript(ddl)
    conn.commit()
    conn.close()
