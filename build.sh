#!/bin/sh
# See https://share.getty.edu/display/SOFTARCH/Using+the+Nexus+Package+Manager+with+Getty+Packages for how to configure twine to publish
# Install the build requirements too! (twine, wheel)
pip install -r build_requirements.txt

rm -Rrf dist/*

## build the final version
python -m build

## upload it
twine upload -r getty dist/*
