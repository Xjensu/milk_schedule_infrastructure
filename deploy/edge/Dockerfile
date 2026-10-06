FROM hashicorp/consul-template:0.41.2 AS template
FROM nginx:1.28.0-alpine
RUN apk add --no-cache python3 iptables
COPY --from=template /bin/consul-template /usr/local/bin/consul-template
COPY nginx.conf /etc/nginx/nginx.conf
COPY upstreams.ctmpl /etc/nginx/upstreams.ctmpl
COPY denylist.geo /etc/nginx/denylist.geo
COPY supervise.py /opt/edge/supervise.py
ENTRYPOINT ["python3", "/opt/edge/supervise.py"]
