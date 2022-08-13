FROM amazonlinux:2.0.20210126.0

RUN yum -y groupinstall "Development Tools" && \
yum -y install openssl-devel bzip2-devel libffi-devel && \
yum -y install wget && \
wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz && \
yum install -y tar && \
yum install -y gzip && \
tar xvf Python-3.8.7.tgz && \
cd Python-3.8*/ && \
./configure --enable-optimizations && \
make altinstall && \
yum install -y zip && \
yum clean all


RUN python3.8 -m pip install --upgrade pip && \
python3.8 -m pip install virtualenv

RUN python3.8 -m venv myvenv
RUN source myvenv/bin/activate

RUN pip install requests==2.26.0 -t ./python
RUN pip install selenium==4.1.0 -t ./python
#RUN pip install webdriver-manager==3.5.3 -t ./python
RUN pip install beautifulsoup4==4.10.0 -t ./python
RUN pip install lxml==4.9.1 -t ./python
#RUN pip install tqdm==4.63.0 -t ./python
RUN pip install firebase-admin==5.2.0 -t ./python

# RUN deactivate
RUN zip -r python.zip ./python/


# docker build -f aws_lambda_env/python3.8.7.Dockerfile --tag aws-lambda-library:1.0 .
# docker cp container_name:python.zip .
