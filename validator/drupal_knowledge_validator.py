import yaml


def _extract_docs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return list(yaml.safe_load_all(f))
    except Exception:
        return []


def evaluate_drupal_knowledge(file_path):
    """Return Drupal knowledge score for one output file."""
    docs = _extract_docs(file_path)

    if not docs:
        return 0

    score = 0
    max_score = 4

    # 1. Config naming (node.type, field.storage, views.view)
    has_names = any(
        isinstance(doc, dict) and any(key.startswith('node.type.') or key.startswith('field.storage.') or key.startswith('views.view.') for key in doc.keys())
        for doc in docs if isinstance(doc, dict)
    )
    if has_names:
        score += 1

    # 2. Module dependencies (simple check for core/dependencies in recipe)
    has_dependencies = False
    for doc in docs:
        if isinstance(doc, dict):
            for key, value in doc.items():
                if key == 'dependencies' or (isinstance(value, dict) and 'dependencies' in value):
                    has_dependencies = True
    if has_dependencies:
        score += 1

    # 3. Field definitions (at least one field.storage and one field.field)
    has_field_storage = any(
        any(isinstance(k, str) and k.startswith('field.storage.') for k in doc.keys())
        for doc in docs if isinstance(doc, dict)
    )
    has_field_config = any(
        any(isinstance(k, str) and k.startswith('field.field.') for k in doc.keys())
        for doc in docs if isinstance(doc, dict)
    )
    if has_field_storage and has_field_config:
        score += 1

    # 4. Views config structure
    has_views = any(
        any(isinstance(k, str) and k.startswith('views.view.') for k in doc.keys())
        for doc in docs if isinstance(doc, dict)
    )
    if has_views:
        score += 1

    return int((score / max_score) * 100)
