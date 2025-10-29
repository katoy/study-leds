/*
  Blink-OTA (ESP32 DevKitC v4 用)

  GPIO4 ピンに接続した外付け LED を 1 秒ごとに点滅させるサンプルです。
  OTA (Over The Air) アップデート機能を追加しています。
  配線例や詳細は README.md を参照してください。
*/

#include <WiFi.h>
#include <ArduinoOTA.h>

// --- WiFi 設定 ---
const char* ssid = "TP-Link_C390";         // WiFi SSID
const char* password = "78986183"; // WiFi パスワード

// --- 設定定数 ---
const int LED_PIN = 4;         // LED 接続ピン番号
const unsigned long INTERVAL = 200; // 点滅間隔 (ミリ秒)

void setup() {
  // LED ピンを出力モードに設定
  pinMode(LED_PIN, OUTPUT);

  // シリアル開始
  Serial.begin(115200);
  Serial.println("Booting");

  // WiFi 接続
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi Connect Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // OTA 設定
  ArduinoOTA.setHostname("esp32-blink-ota");
  ArduinoOTA.begin();
}

void loop() {
  ArduinoOTA.handle(); // OTA アップデート処理

  digitalWrite(LED_PIN, HIGH);  // LED を点灯
  delay(INTERVAL);              // 点灯間隔
  digitalWrite(LED_PIN, LOW);   // LED を消灯
  delay(INTERVAL);              // 消灯間隔
}
