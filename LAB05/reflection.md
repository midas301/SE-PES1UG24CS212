Reflection

1. Which issues were easiest and hardest to fix? Flake8 issues and Pylint naming and docstrings were easiest because they are mechanical. The SQL injection was harder because I had to understand why string formatting is dangerous and rewrite the query with placeholders.

2. Did the tools report any false positives? The hardcoded password warning was low risk because the variable was never used, but it is still bad practice. Tools only guess intent, so a human must judge each warning.

3. How would you integrate static analysis into a workflow? Run the tools as pre-commit hooks and as a CI step, for example GitHub Actions, that fails the build on Bandit findings or a low Pylint score.

4. What improved in the code? Security: no SQL injection, no unsafe pickle, no secret in source. Reliability: specific exceptions, commit after update, clear error for unknown ids. Readability: snake_case names, docstrings, no global variable.
