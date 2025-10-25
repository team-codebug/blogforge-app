document.addEventListener('DOMContentLoaded', function () {
	const mdInput = document.getElementById('mdInput');
	const mdPreview = document.getElementById('mdPreview');
	const wordCount = document.getElementById('wordCount');
	const saveStatus = document.getElementById('saveStatus');
	const togglePreview = document.getElementById('togglePreview');
	
	if (!mdInput || !mdPreview) return;

	let autoSaveTimeout;
	let isFullscreen = false;

	// Markdown rendering function using server-side markdown-it-py
	async function renderMarkdown(text) {
		if (!text.trim()) return '<p class="text-slate-400 italic">Start typing to see preview...</p>';
		
		try {
			console.log('Rendering markdown server-side:', text);
			
			// URL encode the markdown text for GET request
			const encodedText = encodeURIComponent(text);
			const response = await fetch(`/posts/render-markdown?text=${encodedText}`, {
				method: 'GET',
				headers: {
					'X-Requested-With': 'XMLHttpRequest'
				}
			});
			
			console.log('Response status:', response.status);
			
			if (!response.ok) {
				const errorText = await response.text();
				console.error('Response error:', errorText);
				throw new Error(`Failed to render markdown: ${response.status}`);
			}
			
			const data = await response.json();
			console.log('Server rendered HTML:', data.html);
			return data.html;
		} catch (error) {
			console.error('Error rendering markdown:', error);
			// Fallback to simple text display
			return `<p class="text-slate-600">${text.replace(/\n/g, '<br>')}</p>`;
		}
	}

	// Fallback markdown renderer for when server-side fails
	function renderMarkdownFallback(text) {
		if (!text.trim()) return '<p class="text-slate-400 italic">Start typing to see preview...</p>';
		
		console.log('Original text:', text);
		let html = text;
		
		// Headers (process in order from largest to smallest)
		html = html.replace(/^### (.*)$/gm, '<h3 class="text-lg font-semibold mt-4 mb-2 text-slate-800">$1</h3>');
		html = html.replace(/^## (.*)$/gm, '<h2 class="text-xl font-bold mt-6 mb-3 text-slate-800">$1</h2>');
		html = html.replace(/^# (.*)$/gm, '<h1 class="text-2xl font-bold mt-8 mb-4 text-slate-800">$1</h1>');
		
		console.log('After header processing:', html);
		
		// Code blocks (process before inline code)
		html = html.replace(/```([\s\S]*?)```/g, '<pre class="bg-slate-100 p-3 rounded-lg overflow-x-auto my-4"><code class="text-sm">$1</code></pre>');
		
		// Inline code
		html = html.replace(/`([^`]+)`/g, '<code class="bg-slate-100 px-1 py-0.5 rounded text-sm font-mono">$1</code>');
		
		// Bold and italic
		html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-slate-800">$1</strong>');
		html = html.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>');
		
		// Strikethrough
		html = html.replace(/~~(.*?)~~/g, '<del class="line-through text-slate-500">$1</del>');
		
		// Horizontal rules
		html = html.replace(/^---$/gm, '<hr class="border-0 border-t border-slate-300 my-6">');
		html = html.replace(/^\*\*\*$/gm, '<hr class="border-0 border-t border-slate-300 my-6">');
		
		// Links
		html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-orange-500 hover:text-orange-600 underline">$1</a>');
		
		// Lists - unordered
		html = html.replace(/^\* (.*$)/gim, '<li class="ml-4 mb-1">$1</li>');
		html = html.replace(/^- (.*$)/gim, '<li class="ml-4 mb-1">$1</li>');
		
		// Lists - ordered
		html = html.replace(/^\d+\. (.*$)/gim, '<li class="ml-4 mb-1">$1</li>');
		
		// Wrap list items in ul/ol
		html = html.replace(/(<li class="ml-4 mb-1">.*<\/li>)/gs, '<ul class="list-disc list-inside my-4">$1</ul>');
		
		// Line breaks and paragraphs
		html = html.replace(/\n\n/g, '</p><p class="mb-3 text-slate-600">');
		html = html.replace(/\n/g, '<br>');
		
		// Wrap remaining text in paragraphs (but not if it's already wrapped)
		html = html.replace(/^(?!<[h1-6]|<ul|<ol|<pre|<li)(.*)$/gm, function(match, content) {
			if (content.trim() && !content.startsWith('<')) {
				return '<p class="mb-3 text-slate-600">' + content + '</p>';
			}
			return match;
		});
		
		// Clean up empty elements
		html = html.replace(/<p class="mb-3 text-slate-600"><\/p>/g, '');
		html = html.replace(/<p class="mb-3 text-slate-600"><br><\/p>/g, '');
		html = html.replace(/<p class="mb-3 text-slate-600">\s*<\/p>/g, '');
		
		console.log('Final HTML:', html);
		return html;
	}

	// Update word count
	function updateWordCount() {
		const text = mdInput.value;
		const words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
		wordCount.textContent = `${words} words`;
	}

	// Auto-save functionality - only for editing existing posts
	function autoSave() {
		// Check if we're editing an existing blog (URL contains /edit)
		const isEditing = window.location.pathname.includes('/edit');
		
		if (!isEditing) {
			// Don't auto-save when creating new blogs
			saveStatus.textContent = 'Draft';
			saveStatus.className = 'text-slate-500';
			return;
		}
		
		if (autoSaveTimeout) clearTimeout(autoSaveTimeout);
		
		saveStatus.textContent = 'Saving...';
		saveStatus.className = 'text-yellow-600';
		
		// Auto-save every 15 seconds when editing
		autoSaveTimeout = setTimeout(async () => {
			try {
				// Get blog ID from form data attribute
				const form = document.querySelector('form[data-blog-id]');
				const blogId = form ? form.getAttribute('data-blog-id') : null;
				
				if (!blogId) {
					console.error('Blog ID not found');
					saveStatus.textContent = 'Save failed';
					saveStatus.className = 'text-red-600';
					return;
				}
				
				// Get form data
				const title = document.querySelector('input[name="title"]').value;
				const description = document.querySelector('textarea[name="description"]').value;
				const content = mdInput.value;
				
				// Send auto-save request to backend
				const response = await fetch('/posts/auto-save', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
					},
					body: JSON.stringify({
						blog_id: blogId,
						title: title,
						description: description,
						content: content
					})
				});
				
				const data = await response.json();
				
				if (response.ok && data.success) {
					saveStatus.textContent = 'Saved';
					saveStatus.className = 'text-green-600';
				} else {
					saveStatus.textContent = 'Save failed';
					saveStatus.className = 'text-red-600';
				}
			} catch (error) {
				console.error('Auto-save error:', error);
				saveStatus.textContent = 'Save failed';
				saveStatus.className = 'text-red-600';
			}
		}, 5000); // 15 seconds
	}

	// Live preview update
	async function updatePreview() {
		const text = mdInput.value;
		const html = await renderMarkdown(text);
		console.log('Setting innerHTML to:', html);
		mdPreview.innerHTML = html;
		console.log('Preview element after setting:', mdPreview.innerHTML);
		console.log('Preview element children:', mdPreview.children);
		console.log('First child tag name:', mdPreview.children[0]?.tagName);
		updateWordCount();
		autoSave();
	}

	// Fullscreen toggle
	function toggleFullscreen() {
		if (!isFullscreen) {
			mdPreview.style.position = 'fixed';
			mdPreview.style.top = '0';
			mdPreview.style.left = '0';
			mdPreview.style.width = '100vw';
			mdPreview.style.height = '100vh';
			mdPreview.style.zIndex = '9999';
			mdPreview.style.backgroundColor = 'white';
			mdPreview.style.padding = '2rem';
			mdPreview.style.overflow = 'auto';
			togglePreview.textContent = 'Exit Fullscreen';
			isFullscreen = true;
		} else {
			mdPreview.style.position = '';
			mdPreview.style.top = '';
			mdPreview.style.left = '';
			mdPreview.style.width = '';
			mdPreview.style.height = '';
			mdPreview.style.zIndex = '';
			mdPreview.style.backgroundColor = '';
			mdPreview.style.padding = '';
			mdPreview.style.overflow = '';
			togglePreview.textContent = 'Fullscreen';
			isFullscreen = false;
		}
	}

	// Event listeners
	mdInput.addEventListener('input', updatePreview);
	mdInput.addEventListener('keydown', function(e) {
		// Tab support for indentation
		if (e.key === 'Tab') {
			e.preventDefault();
			const start = this.selectionStart;
			const end = this.selectionEnd;
			this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
			this.selectionStart = this.selectionEnd = start + 4;
			updatePreview();
		}
	});
	
	if (togglePreview) {
		togglePreview.addEventListener('click', toggleFullscreen);
	}

	// Initialize
	updatePreview();
	
	console.log('Enhanced markdown editor loaded');
});
