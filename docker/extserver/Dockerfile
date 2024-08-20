FROM alpine@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5

RUN apk add --no-cache python3 py3-pip openssh-client shadow

# 새 사용자 생성
RUN adduser -D -u 1001 appuser

# SSH 키 설정
RUN mkdir -p /home/appuser/.ssh
COPY ./src/ssh_keys/ctf_key /home/appuser/.ssh/id_rsa
COPY ./src/ssh_keys/ctf_key.pub /home/appuser/.ssh/id_rsa.pub
RUN chmod 700 /home/appuser/.ssh
RUN chmod 600 /home/appuser/.ssh/id_rsa
RUN chown -R appuser:appuser /home/appuser/.ssh

# 가상 환경 생성 및 활성화
ENV VIRTUAL_ENV=/home/appuser/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 웹 서버 설정 (예: Flask)
WORKDIR /home/appuser/app

COPY ./src/extserver/requirements.txt /home/appuser/app/
RUN pip3 install -r requirements.txt

COPY ./src/extserver/app.py /home/appuser/app/

# 소유권 변경
RUN chown -R appuser:appuser /home/appuser/app

# 포트 노출
EXPOSE 8090

# appuser로 실행
USER appuser

CMD ["python3", "app.py"]