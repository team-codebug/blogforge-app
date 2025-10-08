/** @type {import('tailwindcss').Config} */
module.exports = {
	darkMode: 'class',
	content: [
		'./app/templates/**/*.html',
		'./app/static/js/**/*.js',
	],
	theme: {
		extend: {
			colors: {
				slate: {
					950: '#0b0f19',
				},
				indigo: {
					950: '#1b103f',
				},
				purple: {
					600: '#7c3aed', // electric purple accent
					700: '#6d28d9',
				},
			},
			boxShadow: {
				soft: '0 10px 30px -10px rgba(0,0,0,0.25)'
			},
			transitionProperty: {
				width: 'width',
			},
		},
	},
	plugins: [],
};
