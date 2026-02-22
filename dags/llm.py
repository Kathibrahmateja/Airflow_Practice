from pathlib import Path
path = str(Path(__file__).resolve().parent.joinpath('llm.py'))
print(f"Executing code from:{path} ")
print({Path(path).parent})