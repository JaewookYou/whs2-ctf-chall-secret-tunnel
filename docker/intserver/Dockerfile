FROM alpine@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5

RUN apk add --no-cache openssh-server shadow

RUN adduser -D -u 1001 ctfuser
RUN sed -i 's/ctfuser:!/ctfuser:*/' /etc/shadow

RUN ssh-keygen -A
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
RUN echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config

RUN mkdir -p /home/ctfuser/.ssh
COPY ./src/ssh_keys/id_rsa.pub /home/ctfuser/.ssh/authorized_keys
RUN chmod 700 /home/ctfuser/.ssh
RUN chmod 600 /home/ctfuser/.ssh/authorized_keys
RUN chown -R ctfuser:ctfuser /home/ctfuser/.ssh

RUN mkdir /home/ctfuser/flag
RUN dd if=/dev/urandom of=/home/ctfuser/flag/large_file bs=1M count=100
RUN echo "FLAG{this_is_your_flag}" >> /home/ctfuser/flag/large_file

RUN chown -R ctfuser:ctfuser /home/ctfuser/flag
RUN chmod 755 /home/ctfuser
RUN chmod 744 /home/ctfuser/flag/large_file

COPY ./src/intserver/dari11.jpg /home/ctfuser/dari11.jpg
COPY ./src/intserver/dari22.jpg /home/ctfuser/dari22.jpg
COPY ./src/intserver/dari33.jpg /home/ctfuser/dari33.jpg

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]