# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /root

# Install any needed packages specified in requirements.txt
RUN apt update && apt install curl gpg -y && pip install --no-cache-dir asciinema-automation
RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes && echo 'eval "$(starship init bash)"' >> ~/.bashrc
# starship container module does not currently show name properly
RUN mkdir -p /root/.config && \
    cat <<'EOF' > /root/.config/starship.toml
[container]
format = '[$symbol \[demo\]]($style) '
EOF


# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["bash"]
