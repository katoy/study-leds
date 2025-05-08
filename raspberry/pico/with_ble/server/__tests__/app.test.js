/**
 * @jest-environment jsdom
 */
import * as app from '../js/app.js';

// 共通のHTML構造
const html = `
  <button id="connectBtn"></button>
  <button id="disconnectBtn"></button>
  <div id="controls"></div>
  <button id="ledOnBtn"></button>
  <button id="ledOffBtn"></button>
  <p id="status"></p>
`;

describe('CONFIG', () => {
  test('定数が正しく設定されている', () => {
    expect(app.CONFIG.DEVICE_NAME).toBe('LED-test');
    expect(app.CONFIG.SERVICE_UUID).toBe(0x181A);
    expect(app.CONFIG.CHARACTERISTIC_UUID).toBe(0x2ABF);
  });
});

describe('getElements', () => {
  let elems;
  beforeEach(() => {
    document.body.innerHTML = html;
    elems = app.getElements();
  });

  test('全ての要素が取得できる', () => {
    expect(elems.connectBtn.tagName).toBe('BUTTON');
    expect(elems.disconnectBtn.tagName).toBe('BUTTON');
    expect(elems.controls.tagName).toBe('DIV');
    expect(elems.ledOnBtn.tagName).toBe('BUTTON');
    expect(elems.ledOffBtn.tagName).toBe('BUTTON');
    expect(elems.status.tagName).toBe('P');
  });
});

describe('updateUI', () => {
  let elems;
  beforeEach(() => {
    document.body.innerHTML = html;
    elems = app.getElements();
  });

  test('connected=true の場合 UI が接続中表示', () => {
    app.updateUI(elems, true);
    expect(elems.connectBtn.hidden).toBe(true);
    expect(elems.disconnectBtn.hidden).toBe(false);
    expect(elems.controls.hidden).toBe(false);
    expect(elems.status.textContent).toBe('接続中');
  });

  test('connected=false の場合 UI が切断中表示', () => {
    app.updateUI(elems, false);
    expect(elems.connectBtn.hidden).toBe(false);
    expect(elems.disconnectBtn.hidden).toBe(true);
    expect(elems.controls.hidden).toBe(true);
    expect(elems.status.textContent).toBe('切断中');
  });
});

describe('connectPico', () => {
  let elems;
  beforeEach(() => {
    document.body.innerHTML = html;
    elems = app.getElements();
  });

  test('成功時にdeviceとcharを返しUI更新', async () => {
    const mockChar = {};
    const mockService = { getCharacteristic: jest.fn().mockResolvedValue(mockChar) };
    const mockServer = { getPrimaryService: jest.fn().mockResolvedValue(mockService) };
    const mockDevice = {
      gatt: { connect: jest.fn().mockResolvedValue(mockServer) },
      addEventListener: jest.fn()
    };
    global.navigator.bluetooth = { requestDevice: jest.fn().mockResolvedValue(mockDevice) };

    const result = await app.connectPico(elems);
    expect(result.device).toBe(mockDevice);
    expect(result.char).toBe(mockChar);
    expect(elems.status.textContent).toBe('接続中');
    expect(mockDevice.addEventListener).toHaveBeenCalledWith('gattserverdisconnected', expect.any(Function));
  });

  test('失敗時にエラーを投げる', async () => {
    global.navigator.bluetooth = { requestDevice: jest.fn().mockRejectedValue(new Error('timeout')) };
    await expect(app.connectPico(elems)).rejects.toThrow('接続失敗: timeout');
  });
});

describe('disconnectPico', () => {
  test('接続中ならdisconnectが呼ばれる', () => {
    const mockGatt = { connected: true, disconnect: jest.fn() };
    app.disconnectPico({ gatt: mockGatt });
    expect(mockGatt.disconnect).toHaveBeenCalled();
  });

  test('未接続なら何もしない', () => {
    const mockGatt = { connected: false, disconnect: jest.fn() };
    expect(() => app.disconnectPico({ gatt: mockGatt })).not.toThrow();
    expect(mockGatt.disconnect).not.toHaveBeenCalled();
  });
});

describe('writeLED', () => {
  test('charがないとError', async () => {
    await expect(app.writeLED(null, 1)).rejects.toThrow('未接続');
  });

  test('charがあるとwriteValueが呼ばれる', async () => {
    const mockChar = { writeValue: jest.fn().mockResolvedValue() };
    await app.writeLED(mockChar, 0);
    expect(mockChar.writeValue).toHaveBeenCalledWith(new Uint8Array([0]));
  });
});

describe('setEventListeners', () => {
  let elems;
  beforeEach(() => {
    document.body.innerHTML = html;
    elems = app.getElements();
    ['connectBtn','disconnectBtn','ledOnBtn','ledOffBtn'].forEach(key => {
      elems[key].addEventListener = jest.fn();
    });
  });

  test('全てのbuttonにclickリスナが設定される', () => {
    app.setEventListeners(elems);
    expect(elems.connectBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.disconnectBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.ledOnBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.ledOffBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
  });

  test('connectBtnクリック時にconnectPico成功時の処理が動作する', async () => {
    const connectPicoMock = jest.fn().mockResolvedValue({ device: 'D', char: 'C' });
    app.connectPico = connectPicoMock;
    app.setEventListeners(elems);
    const handler = elems.connectBtn.addEventListener.mock.calls.find(c => c[0] === 'click')[1];
    await handler();
    expect(connectPicoMock).toHaveBeenCalledWith(elems);
    expect(window._bleDevice).toBe('D');
    expect(window._bleChar).toBe('C');
  });

  test('disconnectBtnクリック時にdisconnectPicoが呼ばれる', () => {
    const disconnectPicoMock = jest.fn();
    app.disconnectPico = disconnectPicoMock;
    window._bleDevice = { dummy: true };
    app.setEventListeners(elems);
    const handler = elems.disconnectBtn.addEventListener.mock.calls.find(c => c[0] === 'click')[1];
    handler();
    expect(disconnectPicoMock).toHaveBeenCalledWith(window._bleDevice);
  });

  test('ledOnBtnクリック時にwriteLEDが呼ばれる', async () => {
    const writeLEDMock = jest.fn().mockResolvedValue();
    app.writeLED = writeLEDMock;
    window._bleChar = 'CHAR';
    app.setEventListeners(elems);
    const handler = elems.ledOnBtn.addEventListener.mock.calls.find(c => c[0] === 'click')[1];
    await handler();
    expect(writeLEDMock).toHaveBeenCalledWith('CHAR', 1);
  });

  test('ledOffBtnクリック時にwriteLEDが呼ばれる', async () => {
    const writeLEDMock = jest.fn().mockResolvedValue();
    app.writeLED = writeLEDMock;
    window._bleChar = 'CHAR';
    app.setEventListeners(elems);
    const handler = elems.ledOffBtn.addEventListener.mock.calls.find(c => c[0] === 'click')[1];
    await handler();
    expect(writeLEDMock).toHaveBeenCalledWith('CHAR', 0);
  });

  test('全てのbuttonにclickリスナが設定される', () => {
    app.setEventListeners(elems);
    expect(elems.connectBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.disconnectBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.ledOnBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.ledOffBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
  });
});

describe('initApp', () => {
  test('初期化でUI更新とリスナ設定が行われる', () => {
    document.body.innerHTML = html;
    const elems = app.getElements();
    // spy on addEventListener
    ['connectBtn','disconnectBtn','ledOnBtn','ledOffBtn'].forEach(key => {
      elems[key].addEventListener = jest.fn();
    });

    app.initApp();
    // UI state
    expect(elems.connectBtn.hidden).toBe(false);
    expect(elems.disconnectBtn.hidden).toBe(true);
    expect(elems.controls.hidden).toBe(true);
    expect(elems.status.textContent).toBe('切断中');
    // listeners
    expect(elems.connectBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.disconnectBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.ledOnBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
    expect(elems.ledOffBtn.addEventListener).toHaveBeenCalledWith('click', expect.any(Function));
  });
});
