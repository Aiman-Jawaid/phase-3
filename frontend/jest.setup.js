// Optional: configure or set up a testing framework before each test.
// If you delete this file, remove `setupFilesAfterEnv` from `jest.config.js`

// Used for __tests__/components/ExampleComponent.test.js
import '@testing-library/jest-dom/extend-expect';

// Mock localStorage
Object.defineProperty(window, 'localStorage', {
  value: (() => {
    let store = {};
    return {
      getItem: (key) => store[key] || null,
      setItem: (key, value) => {
        store[key] = value.toString();
      },
      removeItem: (key) => {
        delete store[key];
      },
      clear: () => {
        store = {};
      }
    };
  })(),
  writable: true
});