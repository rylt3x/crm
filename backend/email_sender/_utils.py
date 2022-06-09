from . import _data


def get_smtp_names():
    service_names = []
    for x in _data.SMTP_SERVICES_LIST.values():
        service_names.append(x.get('smtp_name'))
    return service_names


def get_smtp_services():
    services = {}
    for x in _data.SMTP_SERVICES_LIST.values():
        name = x.pop('smtp_name')
        services[name] = x
    return services