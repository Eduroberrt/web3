/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#99E39E",
        secondary: "#1DC8CD",
        midnight_text: "#263238",
        muted: "#d8dbdb",
        error: "#CF3127",
        warning: "#F7931A",
        light_grey: "#505050",
        grey: "#F5F7FA",
        dark_grey: "#1E2229",
        border: "#E1E1E1",
        success: "#3cd278",
        section: "#737373",
        darkmode: "#000510",
        darklight: "#0c372a",
        dark_border: "#959595",
        tealGreen: "#477E70",
        charcoalGray: "#666C78",
        deepSlate: "#282C36",
        slateGray: "#2F3543",
      },
      spacing: {
        '6.25': '6.25rem',
        '8.5': '8.5rem',
        '25': '35.625rem',
        '29': '28rem',
        '45': '45rem',
        '50': '50rem',
        '51': '54.375rem',
        '85': '21rem',
        '94': '22.5rem',
        '120': '120rem',
      },
      maxWidth: {
        'screen-xl': '75rem',
        'screen-2xl': '83.75rem'
      },
      blur: {
        '220': '220px',
        '400': '400px',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
