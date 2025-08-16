#!/usr/bin/env python3
"""
Improved spell and grammar checker for Aptos book markdown files
"""

import re
import sys
import os
from pathlib import Path

# Comprehensive technical terms and common English words to ignore
ALLOWED_WORDS = {
    # Technical terms
    'aptos', 'blockchain', 'cryptocurrency', 'crypto', 'dapp', 'dapps', 
    'sdk', 'api', 'cli', 'json', 'yaml', 'toml', 'typescript', 'javascript',
    'webassembly', 'wasm', 'bcs', 'move', 'sui', 'diem', 'solana', 'ethereum',
    'testnet', 'mainnet', 'devnet', 'fungible', 'nft', 'nfts', 'validator',
    'validators', 'bytecode', 'merkle', 'parallelization', 'serialization',
    'deserialization', 'struct', 'structs', 'enum', 'enums', 'async', 'await',
    'impl', 'mut', 'bool', 'u8', 'u16', 'u32', 'u64', 'u128', 'u256', 'addr',
    'signer', 'vec', 'repo', 'config', 'todo', 'hashmap', 'stdlib', 'framework',
    'cmdline', 'github', 'git', 'npm', 'yarn', 'cargo', 'rust', 'linux', 'macos',
    'ubuntu', 'homebrew', 'gui', 'url', 'urls', 'http', 'https', 'www',
    'localhost', 'dev', 'src', 'bin', 'etc', 'usr', 'var', 'tmp', 'md', 'txt',
    'py', 'js', 'ts', 'rs', 'go', 'cpp', 'hpp', 'html', 'css', 'scss', 'yml',
    'blockstm', 'rocksdb', 'movestdlib', 'aptosstdlib', 'aptosstd', 'tablewithlength',
    'mystruct',
    
    # Common English words that were flagged incorrectly
    'reference', 'references', 'dependencies', 'directly', 'friendly', 'llms',
    'syntax', 'anything', 'mostly', 'constraints', 'constraint', 'apply', 
    'accordingly', 'assembly', 'instructions', 'entry', 'correctly', 'smoothly',
    'cryptographic', 'represented', 'exactly', 'length', 'lengths', 'simply',
    'empty', 'demonstrates', 'demonstrated', 'experience', 'thoroughly', 'system',
    'systems', 'currently', 'quickly', 'python', 'style', 'algorithms', 'constructs',
    'efficiently', 'methods', 'slightly', 'frequently', 'highly', 'especiallly'
}

# Actual misspellings to catch
KNOWN_MISSPELLINGS = {
    'alot': 'a lot',
    'occurence': 'occurrence',
    'recieve': 'receive',
    'seperate': 'separate',
    'definately': 'definitely',
    'accomodate': 'accommodate',
    'acheive': 'achieve',
    'beleive': 'believe',
    'concensus': 'consensus',
    'publically': 'publicly',
    'neccessary': 'necessary',
    'priviledge': 'privilege',
    'occured': 'occurred',
    'begining': 'beginning',
    'commited': 'committed',
    'especiallly': 'especially'  # Found in the files
}

def extract_text_from_markdown(content):
    """Extract plain text from markdown, excluding code blocks and links."""
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]*`', '', content)
    
    # Remove links but keep link text
    content = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', content)
    content = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', content)
    
    # Remove markdown formatting
    content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    content = re.sub(r'__([^_]+)__', r'\1', content)
    content = re.sub(r'_([^_]+)_', r'\1', content)
    
    return content

def check_spelling(text):
    """Check text for actual spelling errors."""
    words = re.findall(r'\b[A-Za-z]+\b', text.lower())
    spelling_errors = []
    
    for word in set(words):  # Use set to avoid duplicates
        if word in KNOWN_MISSPELLINGS:
            spelling_errors.append((word, KNOWN_MISSPELLINGS[word]))
    
    return spelling_errors

def check_grammar(content):
    """Check for common grammar issues."""
    issues = []
    
    # Check for common mistakes
    patterns = [
        (r"\bit's own\b", "its own", "Possessive 'its' doesn't use an apostrophe"),
        (r"\balot\b", "a lot", "Should be two words"),
        (r"\bloose\b.*\b(something|it|them)\b", "lose", "Use 'lose' not 'loose' for the verb"),
        (r"\bthen\b.*\b(better|more|less)\b", "than", "Use 'than' for comparisons"),
    ]
    
    for pattern, suggestion, explanation in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            issues.append((match.group(), suggestion, explanation))
    
    # Check for passive voice overuse (more conservative threshold)
    passive_patterns = re.findall(r'\b(is|are|was|were|be|been|being)\s+\w*ed\b', content, re.IGNORECASE)
    if len(passive_patterns) > 20:  # Raised threshold
        issues.append(('High passive voice', f'{len(passive_patterns)} instances', 'Consider using more active voice'))
    
    return issues

def check_file(file_path):
    """Check a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        text = extract_text_from_markdown(content)
        spelling_errors = check_spelling(text)
        grammar_issues = check_grammar(content)
        
        return spelling_errors, grammar_issues
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return [], []

def main():
    """Main function to check all markdown files."""
    print("🔍 Aptos Book Spell & Grammar Checker")
    print("=" * 50)
    
    md_files = list(Path('.').glob('**/*.md'))
    total_files = len(md_files)
    files_with_issues = 0
    total_spelling_errors = 0
    total_grammar_issues = 0
    
    all_issues = []
    
    for file_path in md_files:
        spelling_errors, grammar_issues = check_file(file_path)
        
        if spelling_errors or grammar_issues:
            files_with_issues += 1
            file_issues = {
                'file': str(file_path),
                'spelling': spelling_errors,
                'grammar': grammar_issues
            }
            all_issues.append(file_issues)
            
            print(f"\n⚠️  {file_path}")
            
            if spelling_errors:
                print("  🔤 Spelling Issues:")
                for word, suggestion in spelling_errors:
                    print(f"    • '{word}' → '{suggestion}'")
                total_spelling_errors += len(spelling_errors)
            
            if grammar_issues:
                print("  📝 Grammar Issues:")
                for issue, suggestion, explanation in grammar_issues:
                    print(f"    • {issue} → {suggestion} ({explanation})")
                total_grammar_issues += len(grammar_issues)
        else:
            print(f"✅ {file_path}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print(f"Total files checked: {total_files}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Files without issues: {total_files - files_with_issues}")
    print(f"Actual spelling errors: {total_spelling_errors}")
    print(f"Grammar concerns: {total_grammar_issues}")
    
    # Detailed issues summary
    if files_with_issues > 0:
        print(f"\n📋 DETAILED ISSUES SUMMARY")
        for issue in all_issues:
            print(f"\n{issue['file']}:")
            if issue['spelling']:
                print("  Spelling:")
                for word, correction in issue['spelling']:
                    print(f"    - {word} → {correction}")
            if issue['grammar']:
                print("  Grammar:")
                for problem, suggestion, explanation in issue['grammar']:
                    print(f"    - {problem} ({explanation})")
    
    if files_with_issues == 0:
        print("\n🎉 All files look good!")
    else:
        print(f"\n⚠️  {files_with_issues} files need attention.")

if __name__ == '__main__':
    main()
