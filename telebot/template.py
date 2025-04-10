import os
import json
from .config import CONFIG_DIR, PREDEFINED_DIR
from .process import stop_bot, start_bot

def apply_template(bot_id, template_index):
    templates = list_templates()
    if template_index < 0 or template_index >= len(templates):
        raise IndexError("Invalid template index")

    chosen_path = templates[template_index]
    with open(chosen_path) as f:
        template = json.load(f)

    keys_to_copy = [
        ('bot', 'long'),
        ('bot', 'short'),
        ('live', 'approved_coins'),
        ('live', 'coin_flags'),
    ]

    bot_config_path = os.path.join(CONFIG_DIR, f"{bot_id}.json")
    with open(bot_config_path) as f:
        bot_config = json.load(f)

    for path in keys_to_copy:
        src = template
        dst = bot_config
        for key in path[:-1]:
            src = src.get(key, {})
            dst = dst.get(key, {})
        dst[path[-1]] = src.get(path[-1], dst.get(path[-1]))
    bot_config['live']['user'] = bot_id

    with open(bot_config_path, 'w') as f:
        json.dump(bot_config, f, indent=4)

    # stop_bot(bot_id)
    # start_bot(bot_id)

def list_templates():
    return [os.path.join(PREDEFINED_DIR, f) for f in os.listdir(PREDEFINED_DIR) if f.endswith('.json')]


def get_available_templates() -> list:
    """获取预定义模板列表"""
    if not os.path.exists(PREDEFINED_DIR):
        return []

    templates = []
    for f in os.listdir(PREDEFINED_DIR):
        if f.endswith(".json"):
            templates.append(f[:-5])  # 去除.json扩展名
    return sorted(templates)