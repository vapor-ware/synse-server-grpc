FROM debian:wheezy-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
  git ca-certificates && \
  rm -rf /var/lib/apt/lists/*

ADD https://github.com/github/hub/releases/download/v2.3.0-pre10/hub-linux-amd64-2.3.0-pre10.tgz /tmp
RUN cd /tmp \
    && tar xzf /tmp/*.tgz \
    && /bin/bash /tmp/hub*/install \
    && rm -rf /tmp/*

WORKDIR /data

ENTRYPOINT ["/usr/local/bin/hub"]