FROM public.ecr.aws/lambda/python:3.9 as build

LABEL maintainer="contact@wookingwoo.com"

RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/97.0.4692.71/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F938549%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/


FROM public.ecr.aws/lambda/python:3.9

LABEL maintainer="contact@wookingwoo.com"

RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

RUN mkdir -p /home/namsigdang-crawler/chromedriver

# Install namsigdnag-crawler dependencies using file requirements.txt
RUN pip install --upgrade pip
COPY requirements.txt  .
RUN pip install -r requirements.txt

COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/

# Copy namsigdang-crawler codes
COPY ./namsigdang_crawler ./

# 실행
CMD [ "lambda_function.lambda_handler" ]

# docker build -f aws_lambda_env/Dockerfile --tag aws-lambda-namsigdang-crawler:1.0 .