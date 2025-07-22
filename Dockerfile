FROM langchain/langgraph-api:3.12



# -- Adding local package . --
ADD . /deps/ISCC_Report_Agent
# -- End of local package . --

# -- Installing all local dependencies --
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*
# -- End of local dependencies install --
ENV LANGSERVE_GRAPHS='{"retrieval_graph": "/deps/ISCC_Report_Agent/src/retrieval_graph/graph.py:graph"}'

WORKDIR /deps/ISCC_Report_Agent