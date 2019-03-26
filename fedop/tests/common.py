import os
from pathlib import Path
import pytest

@pytest.mark.show_testenv
def test_info(capfd, config_file):
    with capfd.disabled():
        django_settings = Path(os.environ['DJANGO_SETTINGS_MODULE']).name
        projroot = str(Path(__file__).parent.parent.parent)
        p = Path(os.environ.get('PVZDLIB_CONFIG_MODULE', 'DEFAULT'))
        pvzdlib_settings = str(p)[len(projroot)+1:]   # reduce to path relative to project root
        print(f"\ntestenv/{__name__}: DJANGO_SETTINGS_MODULE={django_settings}; "
              f"PVZDLIB_CONFIG_MODULE={pvzdlib_settings}")

