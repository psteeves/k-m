from typing import List

import numpy as np

from km.data_models import User
from km.representations.users.base import BaseUserRepresentation


class TopicConcatenator(BaseUserRepresentation):
    def transform(self, users: List[User]) -> List[User]:
        for user in users:
            representation = np.stack(
                [doc.topic_representation for doc in user.documents]
            )
            user.representation = representation

        return users
