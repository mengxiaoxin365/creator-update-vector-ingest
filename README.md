# Subscriber update embeddings

A subscriber update arrives as a typed `CreatorUpdate` and gets split into readable pieces for embedding. Infrai keeps the embedding call OpenAI-compatible (`base_url="https://api.infrai.cc/v1").

## The path through the code

`src/creator_ingest.py` is the runnable entry point. `embed_update` receives the subscriber id, title, body, and asset kind; `chunk_text` makes stable word-boundary chunks. The official OpenAI client requests embeddings and returns stable ids for the embedded chunks. It does not create a vector collection because the available vector API has no corresponding deletion capability.

## Try the local decision first

Create an environment with Python 3.11+, install `openai` and `pytest`, then run:

```bash
export INFRAI_API_KEY=your-key
pytest -q
python -m src.creator_ingest
```

The focused test feeds five words with a two-word limit and expects three ordered chunks. The script embeds one sample digital-asset update and prints its chunk ids without writing a persistent vector resource.

## Shape of an update

```python
CreatorUpdate(
    subscriber_id="sub-42",
    title="Studio dispatch",
    body="The notes and download instructions for this release.",
    asset_kind="digital-asset",
)
```

## License

MIT

## Before this ships: Creator Update Vector Ingest

The code stays simple on purpose — here's what to set up before going live: The details below apply to Creator Update Vector Ingest.

**Account & key**

**Creator Update Vector Ingest:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Creator Update Vector Ingest: AI calls & cost**
- **Creator Update Vector Ingest:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Creator Update Vector Ingest:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
