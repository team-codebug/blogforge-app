async function callAiEndpoint(path, body) {
	const res = await fetch(path, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		credentials: 'same-origin',
		body: JSON.stringify(body || {}),
	});
	if (!res.ok) throw new Error('AI request failed');
	return res.json();
}

export async function summarize(blogId) {
	return callAiEndpoint('/api/ai/summarize', { blog_id: blogId });
}

export async function toLinkedIn(blogId) {
	return callAiEndpoint('/api/ai/blog-to-linkedin', { blog_id: blogId });
}

export async function toTwitter(blogId) {
	return callAiEndpoint('/api/ai/blog-to-twitter-thread', { blog_id: blogId });
}

console.log('ai.js loaded');
