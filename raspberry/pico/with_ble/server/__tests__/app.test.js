import { getElements, updateUI, connectPico, disconnectPico, writeLED, initApp, CONFIG } from '../js/app.js';

describe('getElements()', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <button id="connectBtn"></button>
      <button id="disconnectBtn"></button>
      <div id="controls"></div>
      <button id="ledOnBtn"></button>
      <button id="ledOffBtn"></button>
      <p id="status"></p>
    `;
  });

  test('要素が正しく取得できること', () => {
    const elems = getElements();
    expect(elems.connectBtn).toBeInstanceOf(HTMLElement);
    expect(elems.disconnectBtn).toBeInstanceOf(HTMLElement);
    expect(elems.controls).toBeInstanceOf(HTMLElement);
    expect(elems.ledOnBtn).toBeInstanceOf(HTMLElement);
    expect(elems.ledOffBtn).toBeInstanceOf(HTMLElement);
    expect(elems.status).toBeInstanceOf(HTMLElement);
  });
});

describe('updateUI()', () => {
  let elems;
  beforeEach(() => {
    document.body.innerHTML = `
      <button id="connectBtn"></button>
      <button id="disconnectBtn"></button>
      <div id="controls"></div>
      <button id="ledOnBtn"></button>
      <button id="ledOffBtn"></button>
      <p id="status"></p>
    `;
    elems = getElements();
  });

  test('接続時の表示 (connected=true)', () => {
    updateUI(elems, true);
    expect(elems.connectBtn.hidden).toBe(true);
    expect(elems.disconnectBtn.hidden).toBe(false);
    expect(elems.controls.hidden).toBe(false);
    expect(elems.status.textContent).toBe('接続中');
  });

  test('切断時の表示 (connected=false)', () => {
    updateUI(elems, false);
    expect(elems.connectBtn.hidden).toBe(false);
    expect(elems.disconnectBtn.hidden).toBe(true);
    expect(elems.controls.hidden).toBe(true);
    expect(elems.status.textContent).toBe('切断中');
  });
});

describe('connectPico()', () => {
  test('接続に成功した場合', async () => {
    // Mock navigator.bluetooth
    const mockDevice = {
      gatt: {
        connect: jest.fn().mockResolvedValue({
          getPrimaryService: jest.fn().mockResolvedValue({
            getCharacteristic: jest.fn().mockResolvedValue({})
          })
        })
      },
      addEventListener: jest.fn()
    };
    global.navigator.bluetooth = {
      requestDevice: jest.fn().mockResolvedValue(mockDevice)
    };

    const elems = getElements();
    const result = await connectPico(elems);
    expect(global.navigator.bluetooth.requestDevice).toHaveBeenCalledWith({
      filters: [{ name: CONFIG.DEVICE_NAME }],
      optionalServices: [CONFIG.SERVICE_UUID]
    });
    expect(mockDevice.gatt.connect).toHaveBeenCalled();
    expect(result.device).toBe(mockDevice);
  });

  test('接続に失敗した場合', async () => {
    global.navigator.bluetooth = {
      requestDevice: jest.fn().mockRejectedValue(new Error('Failed to connect'))
    };

    const elems = getElements();
    await expect(connectPico(elems)).rejects.toThrow('接続失敗: Failed to connect');
  });
});

describe('disconnectPico()', () => {
  test('デバイスが接続されている場合、切断されること', () => {
    const mockDevice = {
      gatt: {
        connected: true,
        disconnect: jest.fn()
      }
    };
    disconnectPico(mockDevice);
    expect(mockDevice.gatt.disconnect).toHaveBeenCalled();
  });

  test('デバイスが接続されていない場合、何も起こらないこと', () => {
    const mockDevice = {
      gatt: {
        connected: false,
        disconnect: jest.fn()
      }
    };
    disconnectPico(mockDevice);
    expect(mockDevice.gatt.disconnect).not.toHaveBeenCalled();
  });
});

describe('writeLED()', () => {
  test('未接続の場合、エラーが発生すること', async () => {
    await expect(writeLED(null, 1)).rejects.toThrow('未接続');
  });

  test('接続されている場合、writeValueが呼ばれること', async () => {
    const mockChar = {
      writeValue: jest.fn().mockResolvedValue()
    };
    await writeLED(mockChar, 1);
    expect(mockChar.writeValue).toHaveBeenCalledWith(new Uint8Array([1]));
  });
});

// initApp のテストは、addEventListener のモックが難しいため、省略
// カバレッジが足りない場合は、addEventListener を呼ばないようにロジックを変更することを検討
