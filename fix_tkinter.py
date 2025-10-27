# -*- coding: utf-8 -*-
"""
fix_tkinter.py - Fixes Tkinter Tcl/Tk path issue
Run this BEFORE importing tkinter
"""

import os
import sys

def fix_tkinter_path():
    """
    Fix Tcl/Tk library paths for Python 3.13.
    Call this before importing tkinter.
    """
    # Set Tcl/Tk library paths
    tcl_lib = r"C:\Users\USER\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
    tk_lib = r"C:\Users\USER\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

    # Set environment variables
    os.environ["TCL_LIBRARY"] = tcl_lib
    os.environ["TK_LIBRARY"] = tk_lib

    # Also set for _tkinter
    if hasattr(sys, 'path'):
        tcl_dir = os.path.dirname(tcl_lib)
        if tcl_dir not in sys.path:
            sys.path.insert(0, tcl_dir)

    print(f"[OK] Tcl/Tk paths configured:")
    print(f"  TCL_LIBRARY: {tcl_lib}")
    print(f"  TK_LIBRARY: {tk_lib}")

# Auto-fix when this module is imported
fix_tkinter_path()
