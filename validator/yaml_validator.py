import yaml


def validate_yaml(file_path):
    """Validate YAML file syntax and return score from 0-100."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        yaml.safe_load(content)
        return 100

    except yaml.YAMLError as exc:
        # Minor formatting issues (indentation/unexpected tokens) should map to 70.
        msg = str(exc)
        if 'expected' in msg or 'mapping values are not allowed' in msg or 'found unexpected' in msg:
            return 0
        return 70

    except Exception:
        return 0
