FROM public.ecr.aws/lambda/python:3.9

LABEL maintainer="contact@wookingwoo.com"

RUN mkdir -p /home/namsigdang-crawler/chromedriver

RUN yum install -y wget unzip libX11

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum install -y google-chrome-stable_current_x86_64.rpm

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /home/namsigdang-crawler/chromedriver

# Install namsigdnag-crawler dependencies using file requirements.txt
RUN pip install --upgrade pip
COPY requirements.txt  .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy namsigdnag-crawler codes
COPY ./namsigdang_crawler ${LAMBDA_TASK_ROOT}

# 실행
CMD [ "lambda_function.lambda_handler" ]

# docker build -f aws_lambda_env/Dockerfile --tag aws-lambda-namsigdang-crawler:1.0 .