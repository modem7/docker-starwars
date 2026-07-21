FROM nginxinc/nginx-unprivileged:1.31.3-alpine@sha256:18d67281256ded39ff65e010ae4f831be18f19356f83c60bc546492c7eb6dd23

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