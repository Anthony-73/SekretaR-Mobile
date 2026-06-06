# Speaker Intelligence Block

Speaker Intelligence is responsible for diarization and participant intelligence.

It is a separate block of responsibility. It is not part of Memory. Memory receives processed participant information from this block.

## Initial Behavior

At the first stage, SekretaR does not know participant names.

The system should create anonymous speaker labels:

- `Speaker_1`;
- `Speaker_2`;
- `Speaker_3`;
- additional numbered speakers when needed.

Each anonymous speaker can have a voice fingerprint that may later be matched against speakers from other meetings.

## Responsibilities

- diarization;
- splitting transcript segments by speaker;
- generating voice fingerprints;
- matching similar voices across meetings;
- maintaining anonymous speaker identities;
- supporting gradual participant identification;
- linking repeated speakers across meetings;
- passing participant signals to Memory;
- helping identify authors of decisions and tasks.

## Non-Responsibilities

- long-term user memory ownership;
- project knowledge ownership;
- task lifecycle ownership;
- direct user-facing identity decisions without confirmation.

## Target Flow

Recording -> STT -> Speaker Intelligence -> Structured Transcript -> Summary -> Tasks -> Memory

Speaker Intelligence should improve the quality of downstream summary, task extraction, Memory, and future Assistant behavior by preserving who said what.
