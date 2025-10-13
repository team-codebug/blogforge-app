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
				peach: {
					50: '#fff8f0',
					100: '#fff0e6',
					200: '#ffe0cc',
					300: '#ffd1b3',
					400: '#ffc299',
					500: '#ffb380',
					600: '#ffa366',
					700: '#ff944d',
					800: '#ff8533',
					900: '#ff751a',
				},
				orange: {
					400: '#ff8533',
					500: '#ff751a',
					600: '#e6660f',
				},
				slate: {
					50: '#f8fafc',
					100: '#f1f5f9',
					200: '#e2e8f0',
					300: '#cbd5e1',
					400: '#94a3b8',
					500: '#64748b',
					600: '#475569',
					700: '#334155',
					800: '#1e293b',
					900: '#0f172a',
				},
			},
			backgroundImage: {
				'peach-gradient': 'linear-gradient(180deg, #fff0e6 0%, #ffd1b3 100%)',
			},
			boxShadow: {
				soft: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
				card: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
			},
			transitionProperty: {
				width: 'width',
			},
		},
	},
	plugins: [],
};
