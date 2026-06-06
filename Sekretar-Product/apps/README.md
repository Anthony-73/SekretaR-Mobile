# Apps

Runnable parts of SekretaR live here.

Each app is allowed to have its own runtime, dependencies, deployment unit, and operational lifecycle. Apps may live in one repository and on one physical server at the beginning, but they should keep clear boundaries.

Expected apps:

- `product-api` - public product backend and API entry point.
- `web-app` - web user interface.
- `ai-processing` - Whisper, Local LLM, meeting processing.
- `worker` - queue consumers and background job execution.
- `recorder-android` - Recorder V2 Android product app.
- `admin-console` - future remote administration UI.
