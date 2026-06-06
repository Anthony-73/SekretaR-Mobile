# AI Processing

AI Processing is the local AI computation block.

It runs close to Whisper and Local LLM. It processes meeting artifacts and returns structured results to the product lifecycle through Worker or internal contracts.

Responsibilities:

- audio normalization;
- STT with Whisper;
- handoff to Speaker Intelligence after STT;
- structured transcript preparation after diarization;
- transcript cleanup;
- summary generation;
- task extraction;
- meeting structure extraction;
- memory candidate extraction;
- model run metadata.

Non-responsibilities:

- public user APIs;
- user access rules;
- long-term memory ownership;
- external research;
- client compatibility decisions.

Target processing order:

Recording -> STT -> Speaker Intelligence -> Structured Transcript -> Summary -> Tasks -> Memory
