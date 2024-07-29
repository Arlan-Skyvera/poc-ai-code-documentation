import json

def load_mapping():
    extension_language_map = dict()

    with open('languages.json', 'r') as jsonfile:
        languages: dict = json.load(jsonfile)

        for language, language_info in languages.items():
            _type = language_info.get('type')
            extensions = language_info.get('extensions')

            if not extensions:
                continue

            for extension in extensions:
                extension_language_map[extension] = {
                    'language': language,
                    'type': _type
                }

    return extension_language_map