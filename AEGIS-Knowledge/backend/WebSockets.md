# WebSockets

- Authenticate at connection time (token in the handshake), not by trusting the first message.
- Design an explicit reconnect/resume protocol — connections will drop; don't assume state survives.
- Heartbeat/ping-pong to detect dead connections proactively rather than waiting for a TCP timeout.
- Backpressure matters — a slow consumer can OOM a naive broadcast implementation; bound queues per connection.
