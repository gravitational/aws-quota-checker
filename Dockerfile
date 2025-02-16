FROM python:3.12-alpine
LABEL org.opencontainers.image.source https://github.com/brennerm/aws-quota-checker
RUN apk upgrade
WORKDIR /app
ADD setup.py /app
ADD README.md /app
ADD LICENSE /app
ADD Dockerfile /app
ADD aws_quota /app/aws_quota
RUN pip install .[prometheus]
RUN adduser --disabled-password aqc
USER aqc
ENTRYPOINT ["aws-quota-checker"]
CMD "--help"
