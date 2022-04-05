import yaml
from okro_python import get_environment_info

global env_data


def init_env():
    """
    populate env_data parameter that will contain
    all environment information taken from local config file and okro config
    file
    :return:
    """
    non_okro_config = None
    try:
        non_okro_config = yaml.load(
            open('tests/env/config_data.yml'), Loader=yaml.BaseLoader
        )
    except FileNotFoundError:
        print(
            (
                'Could not find environment file called config_data.yml.'
                'Maybe the File doesn\'t exists?'
            )
        )
    config_okro_info = get_environment_info()

    global env_data
    if non_okro_config:
        env_data = {**non_okro_config, **config_okro_info}
    else:
        env_data = config_okro_info


def get_env():
    if not env_data:
        raise Exception('Could not find environment data')
    return env_data
