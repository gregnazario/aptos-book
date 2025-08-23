import re
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="Convert glossary markdown format.")
parser.add_argument("glossary_path", nargs="?", default="src/appendix/glossary.md",
                    help="Path to the glossary markdown file (default: src/appendix/glossary.md)")
args = parser.parse_args()

p = Path(args.glossary_path)
text = p.read_text(encoding='utf-8')

pattern = re.compile(r'^\*\*(.+?)\*\*\r?\n: (.+)$', re.MULTILINE)
new_text, n = pattern.subn(r'## \1\n\2', text)

print(f'Converted {n} terms.')
p.write_text(new_text, encoding='utf-8')
