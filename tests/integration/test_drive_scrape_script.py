from argparse import Namespace

from scripts.scrape_drive import run


def test_drive_scrape_script(tmpdir):
    files_output_path = tmpdir / "files.json"
    users_output_path = tmpdir / "users.json"
    args = Namespace(
        files_output=files_output_path, users_output=users_output_path, max_num_files=1
    )

    run(args)

    assert files_output_path.exists()
    assert users_output_path.exists()
