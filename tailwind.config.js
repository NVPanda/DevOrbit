module.exports = {
  content: [
    './application/src/templates/**/*.{html,js}',  // Apontar para seus templates HTML e JS
    './application/src/static/**/*.{js,css}' // Encontrar classes em arquivos JS e CSS na pasta static
  ],
  theme: {
    extend: {
      animation: {
        'ping-lento': 'ping-lento 5s cubic-bezier(0.0, 0.1, 0.3, 1) infinite',
      },
      keyframes: {
        'ping-lento': {
          '0%': { transform: 'scale(1)', opacity: '1' },
          '75%, 100%': { transform: 'scale(2)', opacity: '0' },
        },
      },
      position: ['hover', 'focus'],
      space: ['hover', 'focus'],
      alignItems: ['hover', 'focus'],
      overflow: ['hover', 'focus'],
      whitespace: ['hover', 'focus'],
      textAlign: ['hover', 'focus'],
      wordBreak: ['hover', 'focus'],
      boxDecorationBreak: ['hover', 'focus'],
      inset: {
        left: {
          left: 10,
          left: 35,
          left: 40,
          right: 10,
        },
      },
      colors: {
        purple: {
          100: '#E5B3E0',
          500: '#9B59B6',
          700: '#6D28D9',
        },
        green: {
          500: '#10B981',
        },
        black: {
          500: '#000',
        },
        white: {
          800: '#fff',
        },
        gray: {
          900: '#111827',
        },
      },
      fontFamily: {
        sans: ['ui-sans-serif', 'system-ui'],
        serif: ['ui-serif', 'Georgia'],
        mono: ['ui-monospace', 'SFMono-Regular'],
        display: ['Oswald'],
        body: ['"Open Sans"'],
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        '3xl': '0 35px 60px -15px rgba(0, 0, 0, 0.3)',
        inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        none: 'none',
      },
      width: {
        '1/7': '14.2857143%',
        '2/7': '28.5714286%',
        '3/7': '42.8571429%',
        '4/7': '57.1428571%',
        '5/7': '71.4285714%',
        '6/7': '85.7142857%',
      },
      spacing: {
        sm: '8px',
        md: '16px',
        lg: '24px',
        xl: '48px',
      },
      top: {
        top: 12,
        top: 35,
        top: 45,
        top: 40,
        top: 50,
      },
      fontSize: {
        xs: '.75rem',
        sm: '.875rem',
        tiny: '.875rem',
        base: '1rem',
        lg: '1.125rem',
        xl: '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem',
        '6xl': '4rem',
        '7xl': '5rem',
      },
      flex: {
        '1': '1 1 0%',
        auto: '1 1 auto',
        initial: '0 1 auto',
        inherit: 'inherit',
        none: 'none',
        '2': '2 2 0%',
      },
    },
  },
  plugins: [],
};
