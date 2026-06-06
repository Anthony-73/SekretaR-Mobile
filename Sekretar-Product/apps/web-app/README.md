# Web App

Web App is the browser interface for SekretaR.

The current UI Foundation is the restored SekretaR product frontend from the
server backup `sekretar_backup_2026-06-04.tar.gz`.

This UI is now treated as an official product UX contract for Sekretar-Product.
It is intentionally preserved without redesign, framework migration, or backend
adapter replacement at this stage.

Target architecture rule: Web App communicates with Product API only. It must
not call AI Processing, Worker, Memory, or Research services directly. The
restored frontend still contains legacy endpoint calls that will be routed
through compatibility adapters later.

Responsibilities:

- start page and intro video;
- main SekretaR work screen;
- meeting recording and file upload UI;
- Android Recorder launch flow;
- meeting history;
- new meeting notifications;
- meeting result review;
- task confirmation;
- memory and research views when available;
- user-facing status display;
- future assistant and voice UI surfaces.

Current structure:

- `static/index.html` - start page.
- `static/intro.mp4` - intro video.
- `static/app.html` - main product interface.
- `static/css/styles.css` - restored UI styles.
- `static/js/intro.js` - intro flow.
- `static/js/api.js` - legacy product UI logic for recording, upload, results,
  task proposals, and Recorder deep link.
- `static/js/history.js` - legacy history and new meetings UI logic.
- `static/js/beta_access.js` - legacy beta access and local device/user
  identifier logic.
- `static/downloads/sekretar-recorder-beta.apk` - restored Android Recorder
  download asset.

Legacy backend dependencies still present in the restored UI:

- `/upload`
- `/meeting/{meeting_id}`
- `/history/{user_id}`
- `/meetings/new/{user_id}`
- `/beta/check`
- `/beta/activate`
- `/downloads/sekretar-recorder-beta.apk`
- headers `device-id` and `user-id`
- deep link `sekretar://record`
