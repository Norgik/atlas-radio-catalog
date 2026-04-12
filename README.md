# 📻 Bølge — Station Catalog

> The open radio station catalog powering [Bølge](https://apps.apple.com/app/bolge) — the world's radio, in print.

## What is this?

This repository contains the curated catalog of radio stations used by the Bølge iOS app. The catalog is fetched remotely, which means stations can be updated without requiring an app update.

## Structure

```json
{
  "version": 4,
  "updatedAt": "2026-04-11T00:00:00Z",
  "countries": [
    {
      "countryCode": "NO",
      "country": "Norway",
      "stations": [
        {
          "id": "no-nrk-p1",
          "name": "NRK P1",
          "genre": "news talk",
          "language": "no",
          "streamUrl": "https://..."
        }
      ]
    }
  ]
}
```

## Contributing

Want to add a station or fix a stream URL?

1. Fork this repository
2. Edit `remote_catalog.json`
3. Follow the station format above
4. Open a Pull Request

### Station requirements
- Public stream URL (no authentication required)
- Stable and reliable stream
- Correct `language` code (ISO 639-1)
- Correct `genre` tag

## Coverage

Currently **67 countries**, **1088+ stations** across news, talk, music and sport.

## License

Station metadata is provided as-is. Stream URLs belong to their respective broadcasters.
