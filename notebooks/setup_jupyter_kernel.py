"""
Setup script to register the uv environment as a Jupyter kernel.
Run this once to make your uv environment available in Jupyter.
"""
import sys
import subprocess
from pathlib import Path

def setup_kernel():
    """Register the current uv environment as a Jupyter kernel"""
    kernel_name = "youtube-stock-screener"
    python_path = sys.executable
    
    print(f"Registering Jupyter kernel '{kernel_name}'")
    print(f"Python path: {python_path}")
    
    # Install ipykernel if not already installed
    try:
        import ipykernel
        print("✓ ipykernel is installed")
    except ImportError:
        print("Installing ipykernel...")
        subprocess.check_call([python_path, "-m", "pip", "install", "ipykernel"])
    
    # Register the kernel
    try:
        subprocess.check_call([
            python_path, "-m", "ipykernel", "install",
            "--user",
            "--name", kernel_name,
            "--display-name", "Python (legal-ai)"
        ])
        print(f"\n✓ Kernel '{kernel_name}' registered successfully!")
        print(f"\nTo use this kernel:")
        print(f"  1. Start Jupyter: uv run jupyter lab")
        print(f"  2. Open your notebook")
        print(f"  3. Select kernel: Kernel -> Change Kernel -> Python (legal-ai)")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error registering kernel: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_kernel()
