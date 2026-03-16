import yaml


def evaluate_pipeline_setup(file_path):
    """Return score (0-100) based on AI pipeline and module wiring clues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return 0

    # Simple heuristic: check keywords related to ai pipeline.
    keywords = ['ai', 'pipeline', 'prompt', 'api', 'client', 'service', 'handler', 'processor']
    found = sum(1 for kw in keywords if kw in content.lower())
    score = min(100, int((found / len(keywords)) * 100))

    # detect Drupal-specific integration blocks in YAML structure
    try:
        data = yaml.safe_load(content)
        if isinstance(data, dict) and any(k in data for k in ['services', 'routing', 'module']):
            score = max(score, 50)
    except Exception:
        pass

    return score
