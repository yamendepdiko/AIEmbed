from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.5'
DESCRIPTION = 'Python library designed to simplify client-side interaction with deep learning models that perform embedding calculations.'
LONG_DESCRIPTION = 'With this library, users can easily interface with APIs that provide embedding services, allowing them to quickly generate high-quality embeddings for a wide range of natural language processing (NLP) tasks. Whether you need to perform sentiment analysis, semantic similarity matching, or any other task that requires the use of embeddings, Embedding Client makes it easy to access the power of deep learning models from within your Python environment.'

# Setting up
setup(
    name="infrabed",
    version=VERSION,
    author="DepDiko",
    author_email="<yamen.habib@depdiko.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'embedding', 'deep learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)