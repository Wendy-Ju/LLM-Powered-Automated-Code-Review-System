# Phase 1: Code Parsing and Feature Extraction

import ast
import hashlib
from collections import defaultdict, Counter

class CodeAnalyzer:
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)
        self.lines = code.splitlines()

    def get_function_lengths(self):
        """Return the line length of each function."""
        func_lengths = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                start = node.lineno
                end = max(getattr(n, 'lineno', start) for n in ast.walk(node))
                func_lengths[node.name] = end - start + 1
        return func_lengths

    def get_cyclomatic_complexity(self):
        """Return a rough cyclomatic complexity score per function."""
        complexity = defaultdict(int)
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                complexity[node.name] += 1  # function entry point
                for sub in ast.walk(node):
                    if isinstance(sub, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.And, ast.Or)):
                        complexity[node.name] += 1
        return dict(complexity)

    def detect_code_duplication(self, min_lines=3):
        """Detect simple duplication by hashing code blocks."""
        hash_counts = Counter()
        block_hash_map = {}

        for i in range(len(self.lines) - min_lines + 1):
            block = "\n".join(self.lines[i:i + min_lines])
            block_hash = hashlib.md5(block.strip().encode()).hexdigest()
            hash_counts[block_hash] += 1
            if block_hash not in block_hash_map:
                block_hash_map[block_hash] = block

        duplicated = {block_hash_map[h]: c for h, c in hash_counts.items() if c > 1}
        return duplicated


# Example usage
if __name__ == "__main__":
    with open("example.py", "r") as f:
        code = f.read()
    
    analyzer = CodeAnalyzer(code)
    
    print("Function Lengths:")
    print(analyzer.get_function_lengths())
    
    print("\nCyclomatic Complexity:")
    print(analyzer.get_cyclomatic_complexity())
    
    print("\nDuplicate Code Blocks (min 3 lines):")
    duplicates = analyzer.detect_code_duplication()
    for block, count in duplicates.items():
        print(f"Appears {count} times:\n{block}\n{'-' * 30}")

# Phase 2: LLM-Powered Code Review System

import openai
import tiktoken
import time
import logging

openai.api_key = "This is secret." # Insert your secret API key here.

def count_tokens(text, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

class LLMReviewer:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.history = []

    def review_code(self, code: str):
        prompt = (
            "You are a professional software engineer. "
            "Please review the following Python code and provide detailed, constructive feedback, "
            "covering correctness, readability, style, modularity, documentation, and security risks.\n\n"
            f"{code.strip()}"
        )

        tokens_prompt = count_tokens(prompt)

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior software engineer performing a code review."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=512
            )

            text = response.choices[0].message.content.strip()
            usage = response.usage

            self.history.append({
                "input_tokens": tokens_prompt,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "feedback": text,
                "timestamp": time.time()
            })

            return {
                "feedback": text,
                "input_tokens": tokens_prompt,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            }

        except Exception as e:
            return {"error": str(e)}

with open("example.py", "r") as f:
    code = f.read()

reviewer = LLMReviewer()
result = reviewer.review_code(code)

print("=== GPT-3.5 Feedback ===")
print(result["feedback"])
print(f"Tokens used: {result['total_tokens']}")

# Phase 3: Issue Categorization

import re
from collections import defaultdict

# Predefined patterns for categorizing LLM feedback
CATEGORY_PATTERNS = {
    "Style": [
        r"\bPEP8\b", r"indentation", r"naming", r"formatting", r"line length", r"readability"
    ],
    "Bug": [
        r"\bbug\b", r"\berror\b", r"off[- ]by[- ]one", r"\bcrash\b", r"\bunexpected\b",
        r"\bincorrect\b", r"unused variable", r"edge case"
    ],
    "Security": [
        r"SQL injection", r"\bXSS\b", r"hardcoded (secret|password|token)",
        r"vulnerability", r"input validation", r"data sanitization"
    ],
    "Documentation": [
        r"docstring", r"\bcomment\b", r"documentation", r"missing explanation", r"clarity",
        r"explain the function", r"not well documented", r"function description"
    ],
    "Modularity": [
        r"\breusable\b", r"split.*function", r"too long", r"separation of concerns",
        r"single responsibility", r"refactor into smaller functions"
    ]
}

def categorize_feedback(feedback: str) -> dict:
    """
    Categorizes LLM-generated feedback into predefined issue types.
    Parameters:
        feedback (str): The LLM-generated feedback string
    Returns:
        dict: A mapping from category name to a list of matched feedback lines
    """
    categorized = defaultdict(list)
    lines = feedback.strip().splitlines()

    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        for category, patterns in CATEGORY_PATTERNS.items():
            if any(re.search(pattern, cleaned_line, re.IGNORECASE) for pattern in patterns):
                categorized[category].append(cleaned_line)
                break  # Assign to only the first matched category
    return dict(categorized)

def print_categorized_feedback(categorized: dict):
    """
    Nicely prints categorized feedback as numbered lists.
    Parameters:
        categorized (dict): Output from categorize_feedback()
    """
    if not categorized:
        print("No categorizable issues found.")
        return

    for category, items in categorized.items():
        print(f"{category} Issues ({len(items)}):")
        print("-" * (len(category) + 9))
        for idx, issue in enumerate(items, 1):
            print(f"{idx}. {issue}")
        print()

feedback_text = result["feedback"]
categorized = categorize_feedback(feedback_text)
print_categorized_feedback(categorized)

# Phase 4: Static Rule-Based Validation

import re
from collections import defaultdict

class RuleBasedValidator:
    def __init__(self, code: str):
        self.code = code
        self.lines = code.splitlines()
        self.results = defaultdict(list)

    def run_all_checks(self):
        """
        Run all static rule-based code checks.
        Returns:
            dict: category -> list of issue messages
        """
        self.check_hardcoded_secrets()
        self.check_unsafe_functions()
        self.check_missing_type_hints()
        self.check_unused_imports()
        return dict(self.results)

    def check_hardcoded_secrets(self):
        pattern = r"(password|secret|token)\s*=\s*['\"].+['\"]"
        for i, line in enumerate(self.lines):
            if re.search(pattern, line, re.IGNORECASE):
                self.results["Security"].append(
                    f"Line {i + 1}: Hardcoded secret or password → `{line.strip()}`"
                )

    def check_unsafe_functions(self):
        for i, line in enumerate(self.lines):
            if "eval(" in line or "exec(" in line:
                self.results["Security"].append(
                    f"Line {i + 1}: Unsafe use of `eval()` or `exec()` → `{line.strip()}`"
                )

    def check_missing_type_hints(self):
        func_def_pattern = r"def\s+\w+\((.*?)\):"
        for i, line in enumerate(self.lines):
            if re.match(func_def_pattern, line) and "->" not in line:
                self.results["Style"].append(
                    f"Line {i + 1}: Function may be missing return type hint → `{line.strip()}`"
                )

    def check_unused_imports(self):
        imports = {}
        usage = set()
        for i, line in enumerate(self.lines):
            if line.startswith("import ") or line.startswith("from "):
                name = line.split()[1]
                imports[name] = i + 1
            for word in re.findall(r"\b\w+\b", line):
                usage.add(word)

        for name, lineno in imports.items():
            if name not in usage:
                self.results["Style"].append(
                    f"Line {lineno}: Unused import detected → `{self.lines[lineno - 1].strip()}`"
                )

validator = RuleBasedValidator(code)
static_issues = validator.run_all_checks()

for category, issues in static_issues.items():
    print(f"{category} Issues ({len(issues)}):")
    print("-" * (len(category) + 9))
    for issue in issues:
        print(f"- {issue}")
    print()

# Phase 5: Unified Review Result (LLM + Rule-based)

def merge_reviews(llm_categorized: dict, static_validated: dict) -> dict:
    """
    Combine LLM-categorized feedback with rule-based results.
    Prioritizes non-duplicate entries and aligns by category.
    """
    merged = defaultdict(list)

    all_categories = set(llm_categorized) | set(static_validated)
    for category in all_categories:
        lines = set()
        if category in llm_categorized:
            lines.update(llm_categorized[category])
        if category in static_validated:
            lines.update(static_validated[category])
        merged[category] = sorted(lines)

    return dict(merged)

# Combine results from Phase 3 + Phase 4
combined_results = merge_reviews(
    categorize_feedback(result["feedback"]),  # from GPT
    RuleBasedValidator(code).run_all_checks() # from static rules
)

# Print full merged result
print_categorized_feedback(combined_results)