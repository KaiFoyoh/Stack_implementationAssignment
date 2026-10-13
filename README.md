# DCOMP320 — Stack-Based Mathematical Expression Evaluator

## Overview
This Python program reads infix arithmetic expressions from `input.txt`, evaluates them using **two explicit stacks**, and writes the results to `output.txt`. It does not use Python's `eval()`.

## Requirements
- Python 3.9 or later
- No external packages

## Files
- `stack_evaluator.py`: main program, Stack class, tokenizer, evaluator, file processor
- `input.txt`: one expression per line, separated by lines of at least three hyphens
- `output.txt`: generated answers, retaining separator lines
- `test_stack_evaluator.py`: unit tests

## Running the program
1. Install Python and open a terminal in this folder.
2. Run `python stack_evaluator.py` (or `python3 stack_evaluator.py`).
3. Open `output.txt` to inspect the results.
4. To specify alternate files: `python stack_evaluator.py my_input.txt my_output.txt`.
5. To run automated tests: `python -m unittest -v test_stack_evaluator.py`.

## Input rules
- Supported operators: `+`, `-`, `*`, `/`, and parentheses `(` `)`.
- Integers and decimals are accepted; spaces are optional.
- Unary plus and minus are accepted (e.g., `-3 + 5`, `2 * (-3)`).
- A separator is a line of **three or more hyphens**; separator lines and blank lines are preserved.
- Each nonseparator line must contain one complete expression.

## Output and errors
- Integral answers are written without `.0`.
- Nonintegral answers are formatted with up to 12 significant digits.
- Invalid expressions and division by zero produce an `ERROR (line N): ...` line; processing continues.
- Missing input files cause a console error and a nonzero exit status.

## Assumptions and limitations
- Only basic arithmetic is supported; no exponentiation, variables, functions, or implicit multiplication such as `2(3+4)`.
- Numeric computation uses Python floating-point arithmetic, so decimal rounding is possible.
- Separator lines of hyphens must have at least three hyphens.
- Output file is overwritten each time the program runs.

## Algorithm
1. Tokenize and validate the expression.
2. Push numeric operands to a value stack.
3. Push operators to an operator stack; apply higher/equal precedence operators first.
4. Resolve parenthesized subexpressions before continuing.
5. Apply remaining operators and return the single final value.

## GitHub submission
Create a repository, upload these files, then invite your lecturer as a collaborator using the lecturer's GitHub username. Follow your institution's sharing and academic-integrity requirements. Do not add a collaborator until you have their correct account name.
