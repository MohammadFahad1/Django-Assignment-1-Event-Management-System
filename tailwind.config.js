/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //Template at project level
    "./**/templates/**/*.html", //Template at app level
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
