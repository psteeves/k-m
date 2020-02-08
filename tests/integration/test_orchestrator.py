from km.data_models import User


def test_orchestrator(orchestrator):

    orchestrator.fit(max_docs=10)

    bio_query = "Research into diseases of the gut and and breast"

    top_docs = orchestrator.query_documents(bio_query)
    assert len(top_docs) == 10

    # TODO test models work
    top_person = orchestrator.query_people(bio_query)[0]
    assert isinstance(top_person, User)
    other_query = "Space astronaut food nutrients sports goal politics"
    top_person = orchestrator.query_people(other_query)[0][0]
    assert isinstance(top_person, User)
