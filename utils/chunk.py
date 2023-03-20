from typing import List, Tuple


def chunk_corpus(corpus: str, chunk_size: int, sentence_word_count: Tuple[int, int]) -> List[List[str]]:
    all_sentences = []
    count_words = lambda sentence: len(sentence.split(" "))
    sentence_acc = ""

    for sentence in corpus.split(". "):
        if count_words(sentence_acc) + count_words(sentence) > sentence_word_count[1]:
            all_sentences.append(sentence_acc)
            sentence_acc = ""
        sentence_acc += sentence

    if sentence_acc:
        all_sentences.append(sentence_acc)

    # now we have a list of chunks, we need to split them into smaller chunks according to chunk_size
    chunks = []
    for i in range(0, len(all_sentences)):
        chunks.append(all_sentences[i:i + chunk_size])

    return chunks


def show_chunk(chunk):
    for i, sentence in enumerate(chunk):
        print(f"{i + 1} :: {sentence}")
