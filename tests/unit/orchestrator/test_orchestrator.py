from km.metrics.similarity import EuclidianSimilarity
from km.orchestrator.orchestrator import Orchestrator


def test_orchestrator(documents, doc_model, people_model, docs_file):
    orchestrator = Orchestrator(
        document_model=doc_model,
        people_model=people_model,
        similarity_measure=EuclidianSimilarity(),
        docs_path=docs_file,
    )

    orchestrator.fit(documents)

    query = "Research into diseases of the gut and and breast"
    top_docs = orchestrator.query_docs(query)
    top_two_titles = set([d[0].name for d in top_docs[:2]])

    expected_top_two_titles = {"Gut Microbes", "Nanoparticles"}
    assert top_two_titles == expected_top_two_titles
