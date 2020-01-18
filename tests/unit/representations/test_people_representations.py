import numpy as np
import pytest

from km.utils import make_person


@pytest.mark.skip("Disable until DB is created")
def test_document_aggregator(people_model, documents):
    business_documents = [doc for doc in documents if doc.content[:2] == "Be"]
    assert len(business_documents) == 2

    people_model.fit(documents)

    # A specialist should have high variance in expertise
    business_person = make_person([doc.content for doc in business_documents])
    business_person_rep = people_model.transform([business_person])
    assert np.std(business_person_rep) > 0.4

    # A generalist should have low variance in expertise
    generalist_person = make_person([doc.content for doc in documents])
    generalist_person_rep = people_model.transform([generalist_person])
    assert np.std(generalist_person_rep) < 0.1
