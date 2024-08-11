/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ['./**/*.html'],
  theme: {
    fontFamily: {
      'barlow': ["Barlow", 'sans-serif']
    },

    extend: {

      colors: {
        'darkwhite': '#fcfcfd',
        'offwhite': {
          light: '#f2efec',
          DEFAULT: '#eae1d9',
          dark: '#ebe7e3',
        },
      },

    },
  },
  plugins: [],
}
