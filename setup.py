import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rl_plotter",
    version="2.0.0",
    author="Gong Xiaoyu",
    author_email="gxywy@hotmail.com",
    description="A plotter for reinforcement learning (RL)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gxywy/rl-plotter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)