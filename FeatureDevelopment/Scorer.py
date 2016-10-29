from scipy import spatial


class Scorer:


    @staticmethod
    def rank(questions):
        for q in questions:
            scores = []
            for r in questions[q]['related']:
                scores.append(questions[q]['related'][r]['similarity'])
            scores = sorted(scores)
            for r in questions[q]['related']:
                questions[q]['related'][r]['rank'] = scores.index(questions[q]['related'][r]['similarity'])
            # also redo the given ranks, since they skip steps
            scores = []
            for r in questions[q]['related']:
                scores.append(questions[q]['related'][r]['givenRank'])
            scores = sorted(scores)
            for r in questions[q]['related']:
                questions[q]['related'][r]['givenRank'] = scores.index(questions[q]['related'][r]['givenRank'])

    @staticmethod
    def score(questions):
        Scorer.scoreByCosine(questions)


    @staticmethod
    def scoreByCosine(questions):
        for q in questions:
            for r in questions[q]['related']:
                questions[q]['related'][r]['similarity'] = spatial.distance.cosine(questions[q]['featureVector'], questions[q]['related'][r]['featureVector'])
