"""CLI entry point. Subcommands are filled in during later phases."""
import argparse

PLANNED = {
    "run": "Phase 1",
    "regrade": "Phase 1",
    "dry-run": "Phase 1",
    "verify": "Phase 2",
}


def main():
    parser = argparse.ArgumentParser(description="Dead-End agent eval")
    parser.add_argument("command", choices=PLANNED)
    args = parser.parse_args()
    print(f"'{args.command}' is not implemented yet (planned for {PLANNED[args.command]}).")


if __name__ == "__main__":
    main()
