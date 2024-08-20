FROM alpine@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5

RUN apk add --no-cache openssh-server shadow

# 새 사용자 생성 (비밀번호 없이)
RUN adduser -D -u 1001 ctfuser

# SSH 설정
RUN ssh-keygen -A
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
RUN echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config

# SCP 허용 설정
RUN echo "Subsystem sftp internal-sftp" >> /etc/ssh/sshd_config
RUN echo "Match User ctfuser" >> /etc/ssh/sshd_config
RUN echo "  ForceCommand internal-sftp" >> /etc/ssh/sshd_config
RUN echo "  ChrootDirectory /home/ctfuser" >> /etc/ssh/sshd_config
RUN echo "  PermitTunnel no" >> /etc/ssh/sshd_config
RUN echo "  AllowTcpForwarding no" >> /etc/ssh/sshd_config
RUN echo "  X11Forwarding no" >> /etc/ssh/sshd_config

# authorized_keys 설정
RUN mkdir -p /home/ctfuser/.ssh
COPY ./src/ssh_keys/ctf_key.pub /home/ctfuser/.ssh/authorized_keys
RUN chown -R ctfuser:ctfuser /home/ctfuser/.ssh
RUN chmod 700 /home/ctfuser/.ssh
RUN chmod 600 /home/ctfuser/.ssh/authorized_keys

# 플래그 파일 생성 (압축하지 않고 큰 파일 생성)
RUN mkdir /home/ctfuser/flag
RUN dd if=/dev/urandom of=/home/ctfuser/flag/large_file bs=1M count=100
RUN echo "FLAG{this_is_your_flag}" >> /home/ctfuser/flag/large_file

# 권한 설정
RUN chown -R ctfuser:ctfuser /home/ctfuser/flag
RUN chmod 755 /home/ctfuser
RUN chmod 744 /home/ctfuser/flag/large_file

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]