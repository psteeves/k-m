import numpy as np


def test_document_aggregator(user_model, doc_model, bio_user, generalist_user, documents):
    doc_model.fit(documents)
    doc_model.transform(bio_user.documents)
    doc_model.transform(generalist_user.documents)

    # A specialist should have high variance in expertise
    specialist_rep = user_model.transform([bio_user])[0].representation
    assert np.std(specialist_rep) > 0.1

    # A generalist should have low variance in expertise
    generalist_rep = user_model.transform([generalist_user])[0].representation
    assert np.std(generalist_rep) < 0.1
