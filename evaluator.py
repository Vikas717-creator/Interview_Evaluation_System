from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class AnswerEvaluator:

    def __init__(self):

        # load pretrained model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")


    def encode_references(self, reference_answers):
        """
        Encode all reference answers once
        """

        return self.model.encode(reference_answers)


    def evaluate(self, user_answer, reference_embeddings):
        """
        Compare user answer with reference answers
        """

        user_embedding = self.model.encode([user_answer])

        similarities = cosine_similarity(
            user_embedding,
            reference_embeddings
        )[0]

        best_score = np.max(similarities)

        return best_score


    def get_label(self, score):

        if score > 0.75:
            return "Correct"

        elif score > 0.5:
            return "Partially Correct"

        else:
            return "Wrong"
      
    def get_numeric_score(self, score):
      if score > 0.75:
        return 1
      elif score > 0.5:
        return 0.5
      else:
        return 0