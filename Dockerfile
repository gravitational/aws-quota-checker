ARG TARGET_PYTHON_VERSION=3.14.2
ARG TARGET_PYTHON_MINOR=3.14

### Dependencies stage
FROM python:${TARGET_PYTHON_VERSION}-alpine AS builder

RUN pip install pipenv

WORKDIR /app
COPY pyproject.toml Pipfile Pipfile.lock ./

RUN pipenv sync --system

### Runner image
FROM python:${TARGET_PYTHON_VERSION}-alpine

ARG TARGET_PYTHON_MINOR

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python${TARGET_PYTHON_MINOR}/site-packages /usr/local/lib/python${TARGET_PYTHON_MINOR}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY aws_quota /usr/local/lib/python${TARGET_PYTHON_MINOR}/site-packages/aws_quota

# Run as non-root user
RUN adduser --disabled-password aqc
USER aqc

# Run the application
ENTRYPOINT ["aws-quota-checker"]
CMD ["--help"]
