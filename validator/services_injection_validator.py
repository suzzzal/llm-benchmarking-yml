import yaml


def evaluate_services_injection(file_path):
    """Return score (0-100) based on services.yml style injection and definitions."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        data = yaml.safe_load(content)

    except Exception:
        return 0

    score = 0
    quota = 3

    # 1. services key exists
    if isinstance(data, dict) and 'services' in data:
        score += 1

    # 2. service definition exists with class
    def has_real_service(doc):
        if isinstance(doc, dict) and 'services' in doc and isinstance(doc['services'], dict):
            for k, v in doc['services'].items():
                if isinstance(v, dict) and 'class' in v:
                    return True
        return False

    if has_real_service(data):
        score += 1

    # 3. check arguments include @
    has_args = False
    if isinstance(data, dict) and 'services' in data and isinstance(data['services'], dict):
        for svc in data['services'].values():
            if isinstance(svc, dict) and 'arguments' in svc:
                args = svc['arguments']
                if args and any(isinstance(a, str) and a.startswith('@') for a in args):
                    has_args = True
    if has_args:
        score += 1

    return int((score / quota) * 100)
