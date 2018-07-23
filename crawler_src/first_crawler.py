import configparser


def get_config_info():
    """
    :return: Dict
    """
    config = configparser.ConfigParser()
    config.read(filenames='../config.ini', encoding='utf8')
    return config.sections()


if __name__ == '__main__':
    print(get_config_info())
