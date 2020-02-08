from typing import List

import numpy as np

from km.data_models import User
from km.representations.users.base import BaseUserRepresentation


class TopicAggregator(BaseUserRepresentation):
    def transform(self, users: List[User]) -> np.array:
        pass
