
// モジュールとして機能を切り出し
export const CONFIG = {
  DEVICE_NAME: 'LED-test',
  SERVICE_UUID: 0x181A,
  CHARACTERISTIC_UUID: 0x2ABF
};

// DOM要素をまとめて取得
export function getElements() {
  return {
    connectBtn:    document.getElementById('connectBtn'),
    disconnectBtn: document.getElementById('disconnectBtn'),
    controls:      document.getElementById('controls'),
    ledOnBtn:      document.getElementById('ledOnBtn'),
    ledOffBtn:     document.getElementById('ledOffBtn'),
    status:        document.getElementById('status')
  };
}

// UI状態更新
export function updateUI(elements, connected) {
  elements.connectBtn.hidden    = connected;
  elements.disconnectBtn.hidden = !connected;
  elements.controls.hidden      = !connected;
  elements.status.textContent   = connected ? '接続中' : '切断中';
}

// デバイス接続処理
export async function connectPico(elements) {
  const { DEVICE_NAME, SERVICE_UUID, CHARACTERISTIC_UUID } = CONFIG;
  try {
    const device = await navigator.bluetooth.requestDevice({
      filters: [{ name: DEVICE_NAME }],
      optionalServices: [SERVICE_UUID]
    });
    const server  = await device.gatt.connect();
    const service = await server.getPrimaryService(SERVICE_UUID);
    const char    = await service.getCharacteristic(CHARACTERISTIC_UUID);

    device.addEventListener('gattserverdisconnected', () => updateUI(elements, false));
    updateUI(elements, true);
    return { device, char };
  } catch (err) {
    throw new Error(`接続失敗: ${err.message}`);
  }
}

// 切断処理
export function disconnectPico(device) {
  if (device?.gatt.connected) {
    device.gatt.disconnect();
  }
}

// LED書き込み処理
export async function writeLED(char, value) {
  if (!char) {
    throw new Error('未接続');
  }
  await char.writeValue(new Uint8Array([value]));
}

// イベントリスナー設定
export function setEventListeners(elems) {
  elems.connectBtn.addEventListener('click', async () => {
    try {
      const { device, char } = await connectPico(elems);
      // 接続成功後に char を保持
      window._bleDevice = device;
      window._bleChar   = char;
    } catch (e) {
      alert(e.message);
    }
  });

  elems.disconnectBtn.addEventListener('click', () => {
    disconnectPico(window._bleDevice);
  });

  elems.ledOnBtn.addEventListener('click', () => writeLED(window._bleChar, 1).catch(e => alert(e.message)));
  elems.ledOffBtn.addEventListener('click', () => writeLED(window._bleChar, 0).catch(e => alert(e.message)));
}

// 初期化
export function initApp() {
  const elems = getElements();
  updateUI(elems, false);
  setEventListeners(elems);
}

// DOM読み込み後に初期化
// テスト対象から除外
/* istanbul ignore next */
if (!window._test) {
  window.addEventListener('DOMContentLoaded', initApp);
}
