from flask import current_app


def summarize_text(markdown: str) -> str:
	provider = current_app.config.get('AI_PROVIDER', 'openai')
	# TODO: wire to OpenAI or Gemini SDKs
	return 'Summary placeholder'


def blog_to_linkedin(markdown: str) -> str:
	return 'LinkedIn text placeholder'


def blog_to_twitter_thread(markdown: str) -> list[str]:
	return ['Tweet 1 placeholder', 'Tweet 2 placeholder']


def generate_tags(markdown: str) -> list[str]:
	return ['flask', 'ai']
