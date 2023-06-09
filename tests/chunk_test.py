from utils.path import get_absolute_path
from utils.chunk import chunk_corpus, show_chunk


def test_basic_chunking():
    print("Loading corpus...", get_absolute_path("../tests/assets/stalin.txt"))
    with open("../tests/assets/stalin.txt", "r") as f:
        corpus = f.read()

    chunk_size = 16
    sentence_word_count = (15, 30)
    chunked_chunks = chunk_corpus(corpus, chunk_size, sentence_word_count)
    for i, chunk in enumerate(chunked_chunks):
        print(f"======================================== Chunk {i} ========================================")
        show_chunk(chunk)
        print("=========================================================================================\n\n")
    # print("Number of chunks:", len(chunked_chunks))
    # show_chunk(chunked_chunks[0])
    # assert len(chunked_chunks[0]) == chunk_size
    # for all sentences within a random selected chunk the number of words should be less than
    # 30 words
    count_words = lambda sentence: len(sentence.split(" "))
    # for sentence in chunked_chunks[0]:
    #     assert count_words(sentence) <= sentence_word_count[1]
