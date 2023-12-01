#!/bin/bash

# exit when any command fails
set -e

DAY=${1:-$(date +%-d)}
DAY_PADDED=$(printf "%02d" "$DAY")
YEAR=${2:-$(date +%Y)}

mkdir -p "input/day${DAY_PADDED}"

if [[ ! -f "src/day${DAY_PADDED}.py" ]]; then
    sed "s/0/${DAY_PADDED}/g" src/template_day.py >"src/day${DAY_PADDED}.py"
fi

if [[ ! -f "input/day${DAY_PADDED}/input.txt" ]]; then
    aocdl -output "input/day${DAY_PADDED}/input.txt" -day "${DAY}" -year "${YEAR}"
fi

if [[ ! -f "input/example${DAY}.txt" ]]; then
    curl --silent "https://adventofcode.com/${YEAR}/day/${DAY}" | sed -e "s|<em>||" | sed -e "s|</em>||" | xmllint --html --xpath "(//p[contains(., 'example')])[1]/following-sibling::pre[1]/code/text()" - > "input/day${DAY_PADDED}/example.txt"
fi

code "src/day${DAY_PADDED}.py"

xdg-open "https://adventofcode.com/${YEAR}/day/${DAY}"