import numpy as np


def test_doc_representations(doc_model, documents):
    doc_model.fit(documents)
    transformed_docs = doc_model.transform(documents)

    assert len(transformed_docs) == len(documents)

    for doc in transformed_docs:
        # Check topics sum to 1
        np.testing.assert_almost_equal(doc.representation.sum(), 1)
        # All documents are very topic-specific, so the transformed_docs should have high variance
        assert np.std(doc.representation) > 0.4
