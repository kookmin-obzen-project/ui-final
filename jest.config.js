/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */

module.exports = {
    preset: 'ts-jest',

    // Automatically clear mock calls, instances, contexts and results before every test
    clearMocks: true,
  
    // Indicates whether the coverage information should be collected while executing the test
    collectCoverage: false,
  
    // The directory where Jest should output its coverage files
    coverageDirectory: 'coverage',
  
    // Indicates which provider should be used to instrument code for coverage
    coverageProvider: 'v8',
  
    // An array of file extensions your modules use
    moduleFileExtensions: ['js', 'mjs', 'cjs', 'jsx', 'ts', 'tsx', 'json', 'node'],
  
    // A map from regular expressions to module names or to arrays of module names that allow to stub out resources with a single module
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/$1',
    },
  
    // The test environment that will be used for testing
    // testEnvironment: 'jest-environment-node',
    testEnvironment: 'jsdom', 
  
    transform: {
      '^.+\\.{ts|tsx}?$': ['ts-jest', {
        babel: true,
        tsConfig: 'tsconfig.jest.json',
        "useESM": true
      }],
   },

    // The glob patterns Jest uses to detect test files
    testMatch: [
      '<rootDir>/**/*.test.(js|jsx|ts|tsx)',
      '<rootDir>/(tests/unit/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx))',
    ],

    setupFilesAfterEnv: ['<rootDir>/setupTest.js'],
    
    // An array of regexp pattern strings that are matched against all source file paths, matched files will skip transformation
    "transformIgnorePatterns": [
      "/node_modules/(?!(\\/@nivo\\/colors))/"
   ]
   
  };