from setuptools import setup
import os

setup(
    name="mission_control_ml",
    version="0.1.0",
    author="BELBIN BENO RM",
    author_email="belbin.datascientist@gmail.com",
    description="A detached background process monitor with a live-streaming external dashboard for Jupyter.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "Detached ML Process Monitor",
    long_description_content_type="text/markdown",
    url="https://github.com/BELBINBENORM/mission-control-ml",
    py_modules=["mission_control"],
    install_requires=[
        "ipython",
    ],
    classifiers=[
        "Framework :: IPython",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.7',
)
