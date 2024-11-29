FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y curl python3-pip

# For installing selenium
RUN curl -LO https://freeshell.de/phd/chromium/jammy/pool/chromium_130.0.6723.58~linuxmint1+virginia/chromium_130.0.6723.58~linuxmint1+virginia_amd64.deb
RUN apt-get install -y ./chromium_130.0.6723.58~linuxmint1+virginia_amd64.deb
RUN apt-get install -y libasound2

# For rust (not needed presently) later
# RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
# ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /workdir
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY cucumber/ ./cucumber/
COPY scripts/ ./scripts/
COPY telegram_test.py ./

ENTRYPOINT [ ]
CMD [ "python3", "telegram_test.py" ]
