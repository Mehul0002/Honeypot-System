FROM cowrie/cowrie:latest

# Copy custom configuration
COPY cowrie.cfg /cowrie/cowrie-git/cowrie.cfg

# Expose ports
EXPOSE 2222 23
