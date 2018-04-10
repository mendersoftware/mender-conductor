#!/bin/bash
set -u -x -e

body='{
"request": {
"branch":"'"$TRAVIS_BRANCH"'",
"config": {
    "env": {
        "global": {
            "IMAGE_BASE_TAG": "'"$IMAGE_TAG"'"
         }
    }
}
}}'

curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -H "Travis-API-Version: 3" \
    -H "Authorization: token $TRAVIS_TOKEN" \
    -d "$body" \
    https://api.travis-ci.com/repo/mendersoftware%2Fmender-conductor-enterprise/requests
