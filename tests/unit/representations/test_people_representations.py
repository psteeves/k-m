import numpy as np


def test_document_aggregator(people_model, documents):
    business_documents = [doc for doc in documents if doc.text[:2] == "Be"]
    assert len(business_documents) == 2

    people_model.fit(documents)

    # A specialist should have high variance in expertise
    business_person_rep = people_model.transform(business_documents)
    assert np.std(business_person_rep) > 0.4

    # A generalist should have low variance in expertise
    generalist_person_rep = people_model.transform(documents)
    assert np.std(generalist_person_rep) < 0.1
