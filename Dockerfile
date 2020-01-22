FROM mltooling/ml-workspace@sha256:4b68c6a97cb2fc175c649de6a6170a8694770f5c06a610b293a5cbde2f792cd0

# Here we add our desired packages
RUN pip install --no-cache-dir psycopg2-binary
RUN conda install -c plotly plotly-orca

# Remove un-necessary Docker layers
RUN clean-layer.sh
