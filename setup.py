from setuptools import setup


setup(
    name="pyLBL_test_suite",
    version="0.0.0",
    author="R. Menzel",
    author_email="",
    description="Suite of regression and integration tests for pyLBL.",
    url="",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyLBL @ git+http://github.com/GRIPS-code/pyLBL@new_db",
    ],
)
