from pathlib import Path
from agent import run_agent
from cli import parse_args

def main():
    args = parse_args()

    workspace = Path(args.workspace).resolve()

    print("Workspace:", workspace)
    print("Goal:", args.goal)

    result = run_agent(
        goal=args.goal,
        workspace=workspace,
        max_steps=args.max_steps,
        model=args.model
    )

    print("\nFinal response:")
    print(result)


if __name__ == "__main__":
    main()