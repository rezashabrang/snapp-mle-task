#!/bin/bash
find . -name 'maintainability.txt' -delete
radon mi snapp_mle_task -s >>.logs/maintainability.txt
export maintainability=$(radon mi snapp_mle_task -s | grep -Po '(?<=\().*(?=\))' | perl -lane '$a+=$_ for(@F);$f+=scalar(@F);END{print $a/$f}' | xargs printf "%.1f%%\n")
echo "maintainability:" $maintainability
rm -rf assets/images/maintainability.svg
poetry run python3 -m pybadges --left-text="maintainability" --right-color="brightgreen" --right-text=${maintainability} >>assets/images/maintainability.svg
