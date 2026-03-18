module.exports = {
  extends: ["@commitlint/config-conventional"],

  helpUrl:
    "https://github.com/Trung4n/smart-home-uia/blob/main/.gitmessage.txt",

  rules: {
    "type-empty": [2, "never"],
    "subject-empty": [2, "never"],
  },

  formatter: "@commitlint/format", // default formatter
};
