# Issues Found

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608) | Security, Medium | 11 | addTower builds the INSERT query with % string formatting, so a crafted site name can change the SQL | Use a parameterized query with ? placeholders |
| Insecure pickle use (Bandit B403, B301) | Security, Low/Medium | 1, 43 | pickle.loads can execute arbitrary code and serves no purpose here | Remove pickle and return fetchall() directly |
| Hardcoded password (Bandit B105) | Security, Low | 6 | NOC_PASSWORD is stored in source code and never used | Delete it |
| Broad exception (Pylint W0718) | Quality | 20-21 | except Exception hides real errors and prints a vague message | Catch sqlite3.Error and print the error |
| Global statement (Pylint W0603) | Quality | 16 | global service_count makes shared state hard to track | Use a module-level dict STATS |
| Missing commit | Bug | 18-19 | serviceTower updates the database but never commits | Add CONN.commit() |
| Unhandled missing row | Bug | 35-36 | riskLevel raises TypeError if the tower id does not exist | Check for None and raise ValueError |
| Invalid names (Pylint C0103) | Style | 4, 7, 10, 15, 34 | camelCase function names and lowercase module constants | Rename to snake_case and UPPER_CASE |
| Missing docstrings (Pylint C0114, C0116) | Style | module, all functions | No documentation | Add docstrings |
| No else after return (Pylint R1705) | Quality | 36-39 | Unnecessary else after return | Use a conditional expression |
| Too many blank lines (Flake8 E303) | Style | 22-24 | 3 blank lines instead of 2 | Remove one |
| Missing whitespace (Flake8 E225) | Style | 50 | total=len(...) has no spaces around = | Write total = len(...) |
| Line too long (Flake8 E501) | Style | 5, 11, 18, 35, 43 | Lines longer than 79 characters | Wrap lines |
