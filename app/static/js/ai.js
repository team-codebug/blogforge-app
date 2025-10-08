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

export async function summarize(postId) {
	return callAiEndpoint('/api/ai/summarize', { post_id: postId });
}

export async function toLinkedIn(postId) {
	return callAiEndpoint('/api/ai/blog-to-linkedin', { post_id: postId });
}

export async function toTwitter(postId) {
	return callAiEndpoint('/api/ai/blog-to-twitter-thread', { post_id: postId });
}

console.log('ai.js loaded');
