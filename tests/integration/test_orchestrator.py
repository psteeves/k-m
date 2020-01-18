from km.metrics.similarity import EuclidianSimilarity
from km.orchestrator.orchestrator import Orchestrator


def test_orchestrator(doc_model, people_model, data_path):
    orchestrator = Orchestrator(
        document_model=doc_model,
        people_model=people_model,
        similarity_measure=EuclidianSimilarity(),
        data_path=data_path,
    )

    orchestrator.fit()

    bio_query = "Research into diseases of the gut and and breast"

    top_docs = orchestrator.query_documents(bio_query)
    top_two_titles = set([d.title for d in top_docs[:2]])
    expected_top_two_titles = {"Gut Microbes", "Nanoparticles"}
    assert top_two_titles == expected_top_two_titles

    # Disabled until DB creation
    # top_person = orchestrator.query_people(bio_query)[0][0]
    # assert top_person.email == "bio_person@bla.com"
    #
    # other_query = "Space astronaut food nutrients sports goal politics"
    # top_person = orchestrator.query_people(other_query)[0][0]
    # assert top_person.email == "generalist@bla.com"
