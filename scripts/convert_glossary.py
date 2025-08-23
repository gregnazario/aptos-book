import re
from pathlib import Path

p = Path('/Users/greg/git/aptos-book/src/appendix/glossary.md')
text = p.read_text(encoding='utf-8')

pattern = re.compile(r'^\*\*(.+?)\*\*\r?\n: (.+)$', re.MULTILINE)
new_text, n = pattern.subn(r'## \1\n\2', text)

print(f'Converted {n} terms.')
p.write_text(new_text, encoding='utf-8')
