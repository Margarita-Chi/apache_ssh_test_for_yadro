FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Apache2, OpenSSH server and certificates
RUN apt-get update && \
    apt-get install -y --no-install-recommends apache2 openssh-server ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/run/sshd

# Create test user 'tester' with password 'testerpass'
RUN useradd -m -s /bin/bash tester && \
    echo "tester:testerpass" | chpasswd && \
    usermod -aG adm tester 2>/dev/null || true

# Enable password authentication (for testing)
RUN sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config || true
RUN sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config || true

# Copy static site
COPY site/ /var/www/html/

# Fix ownership and permissions
RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

# Copy startup script and make it executable
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Expose SSH and HTTP ports
EXPOSE 22 80

# Run startup script (starts sshd and apache in foreground)
CMD ["/usr/local/bin/start.sh"]

