from __future__ import annotations

import argparse
import json

from .ingestion import load_case
from .reconstruction import build_decision_pack
from .serialization import to_jsonable


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Veyra Decision Evidence Pack from a seed case.")
    parser.add_argument("case_file", help="Path to a JSON seed case.")
    parser.add_argument("--output", "-o", help="Optional output JSON file.")
    args = parser.parse_args()

    events, request = load_case(args.case_file)
    pack = build_decision_pack(events, request)
    payload = json.dumps(to_jsonable(pack), indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.write("\n")
    print(payload)


if __name__ == "__main__":
    main()
