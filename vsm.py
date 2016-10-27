# Imports and setting up the workspace
from gensim import corpora, models, similarities
from collections import defaultdict
import helper_fxns as hf


#############################
# New data is a transformed data set creating bag of words fields out of codes for days.
##############################
def vsm_model(new_data, model='LSI'):
    """
    new_data is a vector of string documents
    """
    documents = new_data
    documents = [hf.strip_punctuation(doc) for doc in documents]
    documents = [' '.join(sorted(doc.split())) for doc in documents]

    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # SORTED
    texts = [sorted(list) for list in texts]
    # SORTED

    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    dictionary = corpora.Dictionary(texts)
    dictionary.save('/tmp/diagnoses.dict')

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('/tmp/diagnoses_corpus.mm', corpus)
    corpus = corpora.MmCorpus('/tmp/diagnoses_corpus.mm')


    tfidf = models.TfidfModel(corpus)
    corpus_model = tfidf[corpus]

    if model == 'LSI':
        lsi = models.LsiModel(corpus_model, id2word=dictionary, num_topics=300)
        corpus_model = lsi[corpus_model]

    index = similarities.MatrixSimilarity(corpus_model)
    index.save('/tmp/diagnoses_similarity_matrix.index')
    index = similarities.MatrixSimilarity.load('/tmp/diagnoses_similarity_matrix.index')

    # sims = index[corpus_tfidf]
    sims = index[corpus_model]
    return sims, documents