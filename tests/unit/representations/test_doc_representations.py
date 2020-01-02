import numpy as np


def test_doc_representations(doc_model, documents):
    doc_model.fit(documents)
    representations = doc_model.transform(documents)

    assert len(representations) == len(documents)

    # Check topics sum to 1
    np.testing.assert_allclose(
        representations.sum(axis=1), np.ones((len(representations)))
    )

    # All documents are very topic-specific, so the representations should have high variance
    for rep in representations:
        assert np.std(rep) > 0.4
