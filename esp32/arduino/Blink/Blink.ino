/*
  Blink (ESP32 DevKitC v4 用)

  GPIO4 ピンに接続した外付け LED を 1 秒ごとに点滅させるサンプルです。
  配線例や詳細は README.md を参照してください。
*/


// --- 設定定数 ---
const int LED_PIN = 4;         // LED 接続ピン番号
const unsigned long INTERVAL = 1000; // 点滅間隔 (ミリ秒)

// 初期化処理 (起動時に 1 回だけ実行)
void setup() {
  // LED ピンを出力モードに設定
  pinMode(LED_PIN, OUTPUT);
}

// メインループ (繰り返し実行)
void loop() {
  digitalWrite(LED_PIN, HIGH);  // LED を点灯
  delay(INTERVAL);              // 点灯間隔
  digitalWrite(LED_PIN, LOW);   // LED を消灯
  delay(INTERVAL);              // 消灯間隔
}
