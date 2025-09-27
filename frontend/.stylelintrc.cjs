module.exports = {
  extends: [
    'stylelint-config-recommended',
    'stylelint-config-tailwindcss',
  ],
  plugins: ['stylelint-order'],
  rules: {
    // Enforce order: custom properties, declarations
    'order/properties-order': [],
    // Warn about unknown at-rules (Tailwind directives are allowed by the plugin)
    'at-rule-no-unknown': [true, { ignoreAtRules: ['tailwind', 'apply', 'variants', 'responsive', 'screen'] }],
    // Allow !important in a few legacy places; project can be tightened later
    'declaration-no-important': null,
    // Allow unknown media feature values like prefers-contrast for broad browser support
    'media-feature-name-value-no-unknown': null,
    // Limit nesting depth to keep CSS readable
    'max-nesting-depth': 3,
  },
  ignoreFiles: ['dist/**', 'node_modules/**'],
};
