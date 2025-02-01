from setuptools import setup, find_packages

setup(
    name="atb",
    version='0.1',
    packages=find_packages(),
    install_requires=["aiohttp"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
