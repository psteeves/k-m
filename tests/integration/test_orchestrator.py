from km.data_models import User


def test_orchestrator(orchestrator):

    orchestrator.fit(max_docs=10)

    bio_query = "Research into diseases of the gut and and breast"

    top_docs = orchestrator.query_documents(bio_query)
    assert len(top_docs) == 8

    # TODO test models work
    top_person = orchestrator.query_users(bio_query)[0]
    assert isinstance(top_person, User)
