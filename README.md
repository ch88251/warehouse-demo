# Warehouse Demo Application

This is a Python CLI application that manages products, inventories, customers and orders. It uses a CLI menu system with submenus for performing typical warehouse 
operations.

## Git Commit Practices

This application follows the practice of leveraging prefixes for all git commit
messages. The benefits of this are as follows:

### Automation & Tooling

* **Automatic change logs:** Scripts can scan prefixes to generate release notes instantly.
* **Semantic Versioning:** Tools automatically determine version bumps (Major, Minor, Patch) based on prefix types (e.g., feat vs fix).
* **Enforced Standards:** Git hooks can reject commits that do not start with an approved prefix.

### List of Common Prefixes

* **feat:** New feature for the user
* **fix:** Bug fix for the application
* **docs:** Documentation-only updates
* **style:** Formatting, white-space, or semi-colon changes that do not affect code meaning
* **refactor:** Code changes that neither fix a bug nor add a feature
* **perf:** Code alterations specifically aimed at improving performance
* **test:** Adding missing tests or correcting existing tests
* **build:** Modifications affecting the build system or external dependencies
* **ci:** Updates to continuous integration configuration files and scripts
* **chore:** Routine maintenance tasks like updating dependencies or tooling