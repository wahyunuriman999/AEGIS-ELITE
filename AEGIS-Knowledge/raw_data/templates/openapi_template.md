# OpenAPI Stub Template

```yaml
openapi: 3.0.0
info:
  title: <Service Name>
  version: 1.0.0
paths:
  /v1/<resource>:
    post:
      summary: Create <resource>
      parameters:
        - in: header
          name: Idempotency-Key
          required: true
          schema: { type: string }
      responses:
        "201": { description: Created }
        "400": { description: Validation error }
        "409": { description: Conflict }
```
