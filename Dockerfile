FROM nginxinc/nginx-unprivileged:1.29.3-alpine

ARG UID=101
ARG GID=101

COPY --chown=$UID:0 --chmod=755 src/ /usr/share/nginx/html/
COPY --chown=$UID:0 --chmod=644 conf/nginx-site.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=10s \
    CMD curl -fSs 127.0.0.1:8080/healthz || exit 1

STOPSIGNAL SIGQUIT

USER $UID

CMD ["nginx", "-g", "daemon off;"]