FROM nginx:1.28.0-alpine
# Python/iptables are used only by the explicitly invoked host firewall helper.
RUN apk add --no-cache python3 iptables
COPY nginx.conf /etc/nginx/nginx.conf
COPY upstreams.conf /etc/nginx/upstreams.conf
COPY errors/ /usr/share/nginx/errors/
COPY denylist.geo /etc/nginx/denylist.geo
CMD ["nginx", "-g", "daemon off;"]
