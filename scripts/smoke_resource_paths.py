import os
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main():
    from PeakDeskSprite.resource_paths import resource_path, resource_root

    expected_root = str(REPO_ROOT)
    actual_root = resource_root()
    if os.path.normcase(os.path.normpath(actual_root)) != os.path.normcase(os.path.normpath(expected_root)):
        raise AssertionError(f"unexpected resource root: {actual_root}")

    language_path = resource_path("res", "language", "language.json")
    if not os.path.isfile(language_path):
        raise AssertionError(f"missing language resource: {language_path}")

    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            before_import_cwd = os.getcwd()
            import run_PeakDeskSprite

            if os.getcwd() != before_import_cwd:
                raise AssertionError("importing run_PeakDeskSprite changed cwd")

            settings_root = run_PeakDeskSprite.settings.BASEDIR
            if os.path.normcase(os.path.normpath(settings_root)) != os.path.normcase(os.path.normpath(expected_root)):
                raise AssertionError(f"unexpected settings.BASEDIR: {settings_root}")
        finally:
            os.chdir(original_cwd)

    print("RESOURCE_PATHS_OK")


if __name__ == "__main__":
    main()
