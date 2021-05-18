from setuptools import find_packages, setup

test_requirements = ["pytest"]

setup(
    name="jinacld_tools",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    version="0.0.2",
    description="Library of helper tools to interact with cloud resources.",
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["wheel"],
    tests_require=open("requirements-dev.txt").readlines(),
    extras_require={
        "test": open("requirements-dev.txt").readlines(),
    },
    author="JinaAI",
)
