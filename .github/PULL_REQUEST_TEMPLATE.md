## What this changes

<!-- One or two sentences. What is different after this PR? -->

## Why

<!-- What was wrong, unclear, or missing? Link the issue if there is one. -->

## Type

- [ ] Fix — something was broken
- [ ] Clarity — an explanation did not land
- [ ] New content — exercise, notebook or module
- [ ] AWS update — behaviour changed
- [ ] Docs / structure

## Checklist

- [ ] Notebooks run start to finish, or state clearly what they need
- [ ] **No credentials, real account IDs, or local paths** in code *or notebook outputs*
- [ ] New exercises include a worked solution
- [ ] Relative links resolve
- [ ] Module `README.md` sequence updated if I added a file to it

## Scrub check

```bash
grep -rlE '[0-9]{12}' --include='*.ipynb' .   # account ids — should only match 123456789012
grep -rl "$(whoami)" --include='*.ipynb' .    # local paths
```

- [ ] Ran the above and it is clean
