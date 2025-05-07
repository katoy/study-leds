module.exports = {
    // JSDOM 環境を利用して DOM API をテスト可能にする
    testEnvironment: 'jest-environment-jsdom',

    // .js ファイルを Babel でトランスパイル
    transform: {
      '^.+\\.js$': 'babel-jest'
    },

    // テストファイルのパターン（__tests__ ディレクトリ以下、.test.js で終わるファイル）
    testMatch: ['**/__tests__/**/*.test.js']
  };
