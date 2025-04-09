main CHANGELOG format:
## [VERSION] Time User: Commit name
### Added
### Modified
### Fixed

VERSION format: Date release + vN.SN.N
vN. - Production release
S   - Build status a-alpha, b-beta, s-stable
N.  - Build version
N   - Git updates




## [9.4.25v0.a1.9] 17:14 Δρ.ΒοροΝ:
Oops...
### Fixed:
- /scr/tests/unit_tests/ - fix import paths from linux



## [9.4.25v0.a1.8] 17:08 Δρ.ΒοροΝ:
fix tests for linux, release first alpha, uptodate CHANGELOG
### Added:
- /scr/builds/ directory, for list of all builds

### Modified:
- /CHANGELOG.md - uptodate this file
- /scr/Makefile - remove clean_cache and run_app commands, rename uptodate to up_req
- rename script /scr/StorageOrigin.py  to  /scr/main.py
- update namespaces in unit_tests

### Fixed:
- /scr/tests/conftest.py - remove 'unv?lid_filepath' test



## [6.4.25v0.a0.7] 23:12 Δρ.ΒοροΝ:
Fast fix N3: Fix long, and maybe unv?lid filepath
### Modified:
- /scr/tests/conftest.py - rename test 'unv>lid_filepath'  to  'unv?lid_filepath'

### Fixed:
- /scr/tests/conftest.py - 'long_filepath' test, for linux



## [6.4.25v0.a0.6] 22:56 Δρ.ΒοροΝ:
Fast fix N2: fixed UNVALID_FILEPATHS for linux
### Modified:
- /scr/tests/conftest.py - rename test 'unv lid_filepath'  to  'unv>lid_filepath'
- /scr/tests/conftest.py - 'long_filepath': change repeats from 100  to  2000



## [6.4.25v0.a0.6] 22:20 Δρ.ΒοροΝ:
Fix abs paths, fix cov path in Makefile, MEGA refactoring and cleening code in StorageOrigin, added new function in SQLiteOrigin, added safemode in JsonOrigin; Tests preparedness is 70-80% now!
### Added:
- /scr/StorageOrigin.py - add full docstrings for all classes; finalised safemode for Json; check_integrity, get_schema, insert_into_page, export/import of json and other for Sqlite3

### Modified:
- /scr/tests/conftest.py - remove Origins fixtures, add constants and added tests from work abs paths
- finalised unit_tests

### Fixed:
- /.github/workflows/python-tests.yml - remove coverage mode
- /scr/Makefile - fix coverage path
- /scr/StorageOrigin.py - remove all None



## [4.4.25v0.a0.5] 9:55 Δρ.ΒοροΝ:
Optimization and preparing
### Added:
- /scr/StorageOrigin.py - optimization, safemode for Json
- /scr/tests/unit_tests/test_StorageOrigin.py - added tests for context manager 'with'

### Fixed:
- /.github/workflows/python-tests.yml - fix requirements path