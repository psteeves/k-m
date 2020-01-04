from km.metrics.similarity import EuclidianSimilarity
from km.orchestrator.orchestrator import Orchestrator


def test_orchestrator(documents, doc_model, people_model, docs_file, people_file):
    orchestrator = Orchestrator(
        document_model=doc_model,
        people_model=people_model,
        similarity_measure=EuclidianSimilarity(),
        docs_path=docs_file,
        people_path=people_file,
    )

    orchestrator.fit()

    bio_query = "Research into diseases of the gut and and breast"

    top_docs = orchestrator.query_docs(bio_query)
    top_two_titles = set([d[0].name for d in top_docs[:2]])
    expected_top_two_titles = {"Gut Microbes", "Nanoparticles"}
    assert top_two_titles == expected_top_two_titles

    top_person = orchestrator.query_people(bio_query)[0][0]
    assert top_person.email == "bio_person@bla.com"

    other_query = "Space astronaut food nutrients sports goal politics"
    top_person = orchestrator.query_people(other_query)[0][0]
    assert top_person.email == "generalist@bla.com"
