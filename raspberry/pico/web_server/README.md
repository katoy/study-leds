

## web-server-002.py の API の呼び出し例

```
curl -X POST http://<PICO_IP>/api/led \
 -H "Content-Type: application/json" \
 -d '{"state": "on"}'

curl -X POST http://<PICO_IP>/api/led \
 -H "Content-Type: application/json" \
 -d '{"state": "off"}'
```

