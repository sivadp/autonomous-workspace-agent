import argparse
from config import DEFAULT_MODEL

def parse_args():
    parser = argparse.ArgumentParser(
        description="Autonomous local workspace agent."
    )

    parser.add_argument("goal")

    parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace root"
    )

    parser.add_argument(
        "--max-steps",
        type=int,
        default=12
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL
    )

    return parser.parse_args()