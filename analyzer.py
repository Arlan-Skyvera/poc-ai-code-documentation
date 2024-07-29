"""
Idea:

1. Use doxygen to generate an automated codebase documentation.
2. Feed the generated documentation to llamaindex.
3. Test LLM regarding the documentation.
"""

import subprocess

def create_config():
    subprocess.run(["doxygen", "-g", "config"])

def run():
    subprocess.run(["doxygen", "config"])

if __name__ == "__main__":
    run()