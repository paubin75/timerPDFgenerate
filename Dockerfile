FROM python:3.9-alpine

# Add your application
# TODO: changer Hello par main
COPY ./hello.py /app/hello.py

# Copy and enable your CRON task
COPY ./crontab /app/crontab
RUN crontab /app/crontab

# Create empty log (TAIL needs this)
RUN touch /tmp/out.log

# Start TAIL - as your always-on process (otherwise - container exits right after start)
CMD crond && tail -f /tmp/out.log