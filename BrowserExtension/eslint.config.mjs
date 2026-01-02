import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  {ignores: ["dist/", "libs/", "toMigrate/", "build.cjs"]},
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  {
      files: ["**/*.{js,mjs,cjs,ts}"],
      languageOptions: { globals: {...globals.browser, ...globals.node} },
      rules: {
          "@typescript-eslint/no-explicit-any": "warn",
          "@typescript-eslint/ban-ts-comment": "off",
          "@typescript-eslint/no-unused-vars": "warn",
          "prefer-const": "warn",
          "@typescript-eslint/no-unsafe-function-type": "warn",
          "@typescript-eslint/no-require-imports": "off",
          "no-setter-return": "warn",
          "no-func-assign": "warn",
          "no-redeclare": "warn",
          "no-constant-condition": "warn",
          "getter-return": "warn",
          "no-prototype-builtins": "warn",
          "no-useless-escape": "warn",
          "no-undef": "off",
          "no-empty": "warn",
          "@typescript-eslint/no-this-alias": "off",
          "@typescript-eslint/no-unused-expressions": "warn",
          "no-useless-catch": "warn",
          "no-cond-assign": "warn"
      }
  }
];
