def configure_imports():
    import os
    import sys

    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    sys.path.append(BASE_DIR)
    sys.path.append(BASE_DIR + '/src/')
