# Dockerfile  -  packages the TravelMind agent for AgentCore Runtime.
# The starter toolkit (agentcore configure/launch) can generate and build this
# for you. It is written out in full here so you can see exactly what it does.

# slim base: small image, short cold start.
FROM python:3.12-slim
WORKDIR /app

# Copy requirements FIRST and install, so Docker caches the (slow) pip layer.
# Changing your code then does not re-run pip.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code.
COPY . .

# The runtime contract: the container must listen on 8080.
EXPOSE 8080

# Start the server. travelmind_runtime.py calls app.run(), which serves
# POST /invocations and GET /ping on 8080.
CMD ["python", "travelmind_runtime.py"]

# What changes in production:
#   - Pin a digest, not just a tag, for the base image (reproducible builds).
#   - Run as a non-root user (add: RUN useradd app && USER app).
#   - Do not bake secrets into the image. Pass creds via the execution role.
