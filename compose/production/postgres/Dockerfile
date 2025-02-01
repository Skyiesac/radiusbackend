FROM postgres:16

# Install PostGIS
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-16-postgis-3 \
        postgresql-16-postgis-3-scripts \
        postgis \
    && rm -rf /var/lib/apt/lists/*


COPY ./compose/production/postgres/extensions.sql /docker-entrypoint-initdb.d/

RUN apt-get update && apt-get install -y gdal-bin
COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/* \
    && mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
