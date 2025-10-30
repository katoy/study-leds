/*
  Blink-OTA-Web (ESP32 DevKitC v4 用)

  GPIO4 ピンに接続した外付け LED を 1 秒ごとに点滅させるサンプルです。
  Web サーバー経由で OTA アップデートが可能です。
  配線例や詳細は README.md を参照してください。
*/

#include <WiFi.h>
#include <WebServer.h>
#include <Update.h>

// --- WiFi 設定 ---
const char* ssid = "TP-Link_C390";
const char* password = "78986183";

// --- 設定定数 ---
const int LED_PIN = 4;
const unsigned long INTERVAL = 1000;

WebServer server(80);

void handleRoot() {
  server.send(200, "text/html", "<h1>ESP32 Blink-OTA Web</h1><a href='/update'>OTA Update</a>");
}

void handleUpdate() {
  server.send(200, "text/html",
    "<form method='POST' action='/update' enctype='multipart/form-data'>"
    "<input type='file' name='update'>"
    "<input type='submit' value='Update'>"
    "</form>");
}

void handleUpdateUpload() {
  HTTPUpload& upload = server.upload();
  if (upload.status == UPLOAD_FILE_START) {
    Serial.printf("Update: %s\n", upload.filename.c_str());
    if (!Update.begin(UPDATE_SIZE_UNKNOWN)) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_WRITE) {
    if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
      Update.printError(Serial);
    }
  } else if (upload.status == UPLOAD_FILE_END) {
    if (Update.end(true)) {
      Serial.printf("Update Success: %u bytes\n", upload.totalSize);
    } else {
      Update.printError(Serial);
    }
  }
}

void handleUpdateSuccess() {
  server.sendHeader("Connection", "close");
  server.send(200, "text/html", "Update Success! Rebooting...");
  delay(1000);
  ESP.restart();
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi Connect Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/update", HTTP_GET, handleUpdate);
  server.on("/update", HTTP_POST, handleUpdateSuccess, handleUpdateUpload);
  server.begin();
}

void loop() {
  server.handleClient();
  digitalWrite(LED_PIN, HIGH);
  delay(INTERVAL);
  digitalWrite(LED_PIN, LOW);
  delay(INTERVAL);
}
