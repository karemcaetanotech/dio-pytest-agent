import argparse, pathlib
from agent import TestGenAgent

def main():
    ap = argparse.ArgumentParser(description="Generate pytest tests from Python code via LangChain + Azure OpenAI.")
    ap.add_argument("--input", "-i", type=str, help="Path to Python file (e.g., samples/math_ops.py)")
    ap.add_argument("--code", "-c", type=str, help="Raw Python code as string (alternative to --input)")
    ap.add_argument("--module-name", "-m", type=str, help="Module name (defaults to file stem or 'user_module')")
    ap.add_argument("--out", "-o", type=str, default=None, help="Output test file path (default tests/test_<module>.py)")
    ap.add_argument("--sys-path-dir", type=str, default=None, help="Relative dir to add to sys.path (e.g., 'samples' or 'src')")
    args = ap.parse_args()

    if not args.input and not args.code:
        ap.error("Provide --input or --code.")

    if args.input:
        p = pathlib.Path(args.input).resolve()
        module_code = p.read_text(encoding='utf-8')
        module_name = args.module_name or p.stem
        default_out = pathlib.Path('tests') / f'test_{p.stem}.py'
    else:
        module_code = args.code
        module_name = args.module_name or 'user_module'
        default_out = pathlib.Path('tests') / f'test_{module_name}.py'

    out_path = pathlib.Path(args.out) if args.out else default_out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    agent = TestGenAgent()
    test_code = agent.generate(module_code, module_name, add_sys_path_dir=args.sys_path_dir)
    out_path.write_text(test_code, encoding='utf-8')
    print(f"✅ Tests written to: {out_path}")

if __name__ == '__main__':
    main()
