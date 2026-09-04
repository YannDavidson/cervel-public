#!/usr/bin/env python3
"""Verify the frozen CERVEL public alpha candidate and release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "release" / "alpha-0.1.0.json"
PYPROJECT = ROOT / "sdk" / "python" / "pyproject.toml"
CHANGELOG = ROOT / "CHANGELOG.md"
RELEASE_NOTES = ROOT / "docs" / "releases" / "0.1.0-alpha.md"
RELEASING = ROOT / "RELEASING.md"


def load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def verify_metadata() -> None:
    manifest = load_manifest()
    python_version = str(manifest["python_version"])
    release_label = str(manifest["release_label"])
    tag = str(manifest["tag"])

    with PYPROJECT.open("rb") as handle:
        project = tomllib.load(handle)["project"]
    if project["version"] != python_version:
        raise SystemExit(f"Python version mismatch: {project['version']} != {python_version}")

    required = {
        CHANGELOG: (release_label,),
        RELEASE_NOTES: (python_version, release_label, tag),
        RELEASING: (python_version, release_label, tag),
    }
    for path, values in required.items():
        text = path.read_text(encoding="utf-8")
        for value in values:
            if value not in text:
                raise SystemExit(f"{path.relative_to(ROOT)} is missing frozen value {value!r}")

    if manifest.get("status") != "prepared-not-published":
        raise SystemExit("release manifest must remain prepared-not-published before explicit release")
    if manifest.get("tag_target_sha") is not None:
        raise SystemExit("tag_target_sha must remain null until the exact post-merge main SHA is selected")

    print(f"PASS metadata freeze: {release_label} / {python_version} / {tag}")


def artifact_files(directory: Path) -> list[Path]:
    files = sorted([*directory.glob("*.whl"), *directory.glob("*.tar.gz")])
    if len(files) != 2:
        raise SystemExit(f"expected exactly one wheel and one sdist in {directory}, found {len(files)}")
    return files


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compare_builds(first: Path, second: Path) -> None:
    first_files = artifact_files(first)
    second_files = artifact_files(second)
    first_map = {path.name: digest(path) for path in first_files}
    second_map = {path.name: digest(path) for path in second_files}
    if first_map != second_map:
        print("FAIL release builds are not byte-for-byte reproducible", file=sys.stderr)
        print(json.dumps({"first": first_map, "second": second_map}, indent=2), file=sys.stderr)
        raise SystemExit(1)
    for name, sha in first_map.items():
        print(f"PASS reproducible {name}: {sha}")


def stage_and_checksum(source: Path, destination: Path) -> None:
    files = artifact_files(source)
    destination.mkdir(parents=True, exist_ok=True)
    for existing in destination.iterdir():
        if existing.is_file():
            existing.unlink()
        elif existing.is_dir():
            shutil.rmtree(existing)
    staged: list[Path] = []
    for artifact in files:
        target = destination / artifact.name
        shutil.copy2(artifact, target)
        staged.append(target)
    checksum_path = destination / "SHA256SUMS"
    checksum_path.write_text(
        "".join(f"{digest(path)}  {path.name}\n" for path in sorted(staged)),
        encoding="utf-8",
    )
    print(checksum_path.read_text(encoding="utf-8"), end="")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("metadata")
    compare = sub.add_parser("compare")
    compare.add_argument("first", type=Path)
    compare.add_argument("second", type=Path)
    stage = sub.add_parser("stage")
    stage.add_argument("source", type=Path)
    stage.add_argument("destination", type=Path)
    args = parser.parse_args()

    if args.command == "metadata":
        verify_metadata()
    elif args.command == "compare":
        compare_builds(args.first, args.second)
    elif args.command == "stage":
        stage_and_checksum(args.source, args.destination)


if __name__ == "__main__":
    main()
