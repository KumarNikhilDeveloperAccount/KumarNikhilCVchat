# Deploy Kumar Nikhil AI CV To A Public Link

This repo is prepared for a two-service Render deployment:

- `kumar-nikhil-ai-cv-engine`
- `kumar-nikhil-ai-cv`

Only the gateway URL needs to be shared with users.

## What Users Will Need

Nothing. They only open the final public HTTPS link in a browser on phone or desktop.

## Before You Start

1. Push this repo to GitHub.
2. Make sure `render.yaml` is in the repo root.

## Deploy On Render

1. Sign in to Render.
2. Choose `New +`.
3. Choose `Blueprint`.
4. Select the GitHub repo containing this project.
5. Render will detect [render.yaml](C:\Users\nkash\OneDrive\Documents\Playground\render.yaml).
6. Approve creation of the two web services.
7. Wait for both services to finish deploying.

## Which Link To Share

Share the public URL of:

- `kumar-nikhil-ai-cv`

Do not share the engine service URL.

## Health Checks

- Gateway health: `/health`
- AI engine health: `/health`

## Notes

- This deployment is currently configured in `mock` mode for the AI engine so it works without paid keys.
- The gateway is the only public app entrypoint.
- The UI is mobile-friendly and does not require installation.

## If Deployment Fails

Check:

1. the gateway service has `AI_ENGINE_URL` populated from the engine service
2. both services show healthy status
3. the shared link is the gateway service URL, not the engine service URL
