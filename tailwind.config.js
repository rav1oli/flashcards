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

      screens: {
        'single': {'min': '416px', 'max': '848px',},
        'double': '848px',
        'triple': '1280px',
      }
    },
  },
  plugins: [],
}
