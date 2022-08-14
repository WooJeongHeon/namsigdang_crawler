docker run -v "$PWD":/var/task "lambci/lambda:build-python3.7" /bin/sh -c "pip install firebase-admin -t python/; exit"


https://aws.amazon.com/ko/premiumsupport/knowledge-center/lambda-layer-simulated-docker/