FROM debian:12-slim

# Install Java and Minecraft dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory (this is where the start.sh script will be mounted)
WORKDIR /minecraft

RUN echo '#!/bin/bash\n\
chmod 755 /minecraft/start.sh\n\
exec "$@"' > /entrypoint.sh && \
    chmod 755 /entrypoint.sh
# Expose Minecraft's default port
EXPOSE 25565

# Command to run the start.sh script
CMD ["bash", "/minecraft/start.sh"]
