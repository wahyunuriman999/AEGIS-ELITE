# API Versioning

- Pick one strategy (URL path `/v1/`, header, or content negotiation) and apply it consistently — don't mix.
- Additive changes (new optional field, new endpoint) don't need a version bump.
- Removing a field, changing a type, or changing required-ness is breaking — needs a new version and a deprecation window for the old one.
- Communicate deprecation with a response header/date, not just documentation nobody reads.
