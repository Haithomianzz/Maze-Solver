from setuptools import setup, find_packages

setup(
    name="MazeSolver",
    version="1.0.0",
    author="Haithomianzz",
    author_email="your_email@example.com",  # Replace with your email
    description="A Python-based application to create and solve mazes using various algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Haithomianzz/Maze-Solver",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "matplotlib",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "maze-solver=main:main",  # Adjust if your entry point is different
        ],
    },
)
