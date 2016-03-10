VocabTool -- (Under development)
===

This is a tool aiming to help with vocabulary learning.

License
---
The core components are published under MIT license.

Current features
---
- Look up words from one source and display the result

Planned features
---
- Cross-platform
- Command line interface
- Interchangeable modules
- Look up words from different sources
- Save entries to local database
- Generate PDF files from entries in the database for recitation

Requirement
---
- Python 3.x
- BeautifulSoup 4
- Requests

Config
---
Configuration is stored in a config.json file(sample config file included). The specific structure depends on the module that uses it. This program does not contain access keys to dictionary APIs, users should apply for their own keys.
