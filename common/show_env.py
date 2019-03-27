import os
from pathlib import Path

def show_env(mod_name):
        django_settings = Path(os.environ['DJANGO_SETTINGS_MODULE']).name
        projroot = str(Path(__file__).parent.parent.parent)
        p = Path(os.environ.get('PVZDLIB_CONFIG_MODULE', 'DEFAULT'))
        pvzdlib_settings = str(p)[len(projroot)+1:]   # reduce to path relative to project root
        print(f"\ntestenv/{mod_name}: DJANGO_SETTINGS_MODULE={django_settings}; "
              f"PVZDLIB_CONFIG_MODULE={pvzdlib_settings}")

