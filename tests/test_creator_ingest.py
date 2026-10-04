from src.creator_ingest import CreatorUpdate, chunk_text


def test_update_chunks_keep_order_and_boundaries():
    update = CreatorUpdate("sub-1", "Dispatch", "one two three four five", "newsletter")
    assert chunk_text(update.body, words_per_chunk=2) == ["one two", "three four", "five"]
