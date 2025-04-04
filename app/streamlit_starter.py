import sys
import os
from streamlit.web import cli

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    doc_py_path = "app/Documentation.py"
    sys.argv = ["streamlit", "run", doc_py_path]
    sys.exit(cli.main())
