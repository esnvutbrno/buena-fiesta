const colors = require('tailwindcss/colors');

module.exports = {
    content: [
        // docker placement of Django application
        '../fiesta/**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                primary: colors.rose['500'],
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
};
