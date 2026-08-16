<!-- chunk_viewer.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chunk Viewer</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: #2e7d32; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .header h1 { margin: 0; }
        .chunk-container { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .chunk-highlight { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 4px; margin: 10px 0; }
        .chunk-meta { display: flex; flex-wrap: wrap; gap: 20px; padding: 10px; background: #e3f2fd; border-radius: 4px; margin-bottom: 15px; }
        .chunk-meta-item { background: white; padding: 5px 10px; border-radius: 4px; }
        .chunk-text { 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            line-height: 1.8; 
            padding: 20px; 
            background: #fafafa; 
            border-radius: 4px;
            font-size: 1rem;
            max-height: none;
            overflow-y: visible;
            border: 1px solid #e0e0e0;
        }
        .other-chunk { background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 4px; border-left: 3px solid #ccc; cursor: pointer; transition: all 0.3s ease; }
        .other-chunk:hover { background: #e8e8e8; transform: translateX(5px); }
        .badge-highlight { background: #ffc107; color: #333; padding: 2px 10px; border-radius: 12px; font-size: 0.7rem; margin-left: 10px; }
        .btn { background: #1976d2; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
        .btn:hover { background: #0d47a1; }
        .btn-success { background: #28a745; }
        .btn-success:hover { background: #1e7e34; }
        .error-box { background: #ffebee; padding: 20px; border-radius: 8px; border-left: 4px solid #dc3545; margin: 10px 0; }
        .loading { text-align: center; padding: 40px; color: #666; }
        .word-count { color: #666; font-size: 0.9rem; margin-left: 10px; }
        .expand-btn { background: #6c757d; color: white; border: none; padding: 4px 12px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
        .expand-btn:hover { background: #5a6268; }
        .full-content { display: block; }
        .chunk-text pre { 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            font-size: 1rem;
            line-height: 1.8;
        }
        .json-download { margin-top: 10px; }
        .json-download a { color: #1976d2; text-decoration: none; }
        .json-download a:hover { text-decoration: underline; }
        .source-link { color: #1976d2; text-decoration: none; }
        .source-link:hover { text-decoration: underline; }
        .chunk-stats { display: flex; gap: 20px; flex-wrap: wrap; margin: 10px 0; }
        .stat-badge { background: #e9ecef; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌱 Crop Calendar AI - Chunk Viewer</h1>
        <p>View complete chunk content from CWWG reports</p>
    </div>

    <div id="app">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 20px;">
            <h2 id="reportName" style="margin: 0;">📄 Loading...</h2>
            <div>
                <button onclick="showAllChunks()" class="btn" style="background: #6c757d;">📋 Show All Chunks</button>
                <button onclick="window.location.reload()" class="btn">🔄 Refresh</button>
            </div>
        </div>
        <div id="chunkList"><div class="loading"><p>⏳ Loading chunk data...</p></div></div>
    </div>

    <script>
        const GITHUB_USERNAME = "Debdotta26";
        const GITHUB_REPO = "crop_calendar_rag";
        const GITHUB_BRANCH = "main";
        const CHUNK_FOLDER = "output/chunks";
        const CHUNK_BASE = `https://raw.githubusercontent.com/${GITHUB_USERNAME}/${GITHUB_REPO}/${GITHUB_BRANCH}/${CHUNK_FOLDER}/`;

        const urlParams = new URLSearchParams(window.location.search);
        const chunkId = urlParams.get('chunk') || '';
        const source = urlParams.get('source') || '';
        let allChunks = [];

        function getChunkFileName(sourceName) {
            let base = sourceName.replace('.pdf', '').trim();
            return `${base}_chunks.json`;
        }

        function loadChunks() {
            if (!source) {
                document.getElementById('reportName').textContent = '❌ No source specified';
                document.getElementById('chunkList').innerHTML = `
                    <div class="error-box">
                        <h3>❌ Missing Source Parameter</h3>
                        <p>Please provide both <code>source</code> and <code>chunk</code> parameters.</p>
                        <p>Example: <code>?source=01-04-2025_Minutes%20of%20the%20meeting%20of%20CWWG%20as%20on%2001.04.2025&chunk=CWWG_00001</code></p>
                    </div>
                `;
                return;
            }

            const fileName = getChunkFileName(source);
            const fileUrl = CHUNK_BASE + encodeURIComponent(fileName);
            document.getElementById('reportName').innerHTML = `📄 <a href="${fileUrl}" target="_blank" class="source-link">${source}</a>`;

            fetch(fileUrl)
                .then(response => {
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    let chunks = [];
                    if (data.chunks && Array.isArray(data.chunks)) chunks = data.chunks;
                    else if (Array.isArray(data)) chunks = data;
                    else { for (let key in data) { if (data[key] && Array.isArray(data[key])) { chunks = data[key]; break; } } }
                    
                    allChunks = chunks;
                    displayChunks(chunks, chunkId);
                })
                .catch(error => {
                    document.getElementById('chunkList').innerHTML = `
                        <div class="error-box">
                            <h3>❌ Error loading chunks</h3>
                            <p><strong>Error:</strong> ${error.message}</p>
                            <p><strong>Attempted URL:</strong> ${fileUrl}</p>
                            <p><strong>Source:</strong> ${source}</p>
                            <p><strong>Chunk ID:</strong> ${chunkId}</p>
                            <p>💡 Make sure the file exists at: <code>${CHUNK_FOLDER}/${fileName}</code></p>
                        </div>
                    `;
                });
        }

        function displayChunks(chunks, targetChunkId) {
            const container = document.getElementById('chunkList');
            const targetChunk = chunks.find(c => c.chunk_id === targetChunkId);
            
            if (!targetChunk) {
                container.innerHTML = `
                    <div class="error-box">
                        <p>❌ Chunk <code>${targetChunkId}</code> not found in this file.</p>
                        <button onclick="showAllChunks()" class="btn">📋 View all chunks</button>
                    </div>
                `;
                return;
            }

            // Get full chunk text - ensure we show everything
            let chunkText = targetChunk.text || 'No text content';
            
            // Count words and characters
            const wordCount = chunkText.split(/\s+/).length;
            const charCount = chunkText.length;

            let html = `
                <div class="chunk-container" style="border: 2px solid #ffc107;">
                    <div class="chunk-highlight">
                        <h3 style="margin: 0; color: #856404;">🎯 Target Chunk: ${targetChunkId}</h3>
                    </div>
                    <div class="chunk-meta">
                        <span class="chunk-meta-item"><strong>Chunk ID:</strong> ${targetChunk.chunk_id}</span>
                        <span class="chunk-meta-item"><strong>Heading:</strong> ${targetChunk.heading || 'N/A'}</span>
                        <span class="chunk-meta-item"><strong>Pages:</strong> ${targetChunk.page_start || 'N/A'} ${targetChunk.page_end ? `- ${targetChunk.page_end}` : ''}</span>
                        <span class="chunk-meta-item"><strong>Words:</strong> ${wordCount}</span>
                        <span class="chunk-meta-item"><strong>Characters:</strong> ${charCount}</span>
                    </div>
                    <div class="chunk-stats">
                        <span class="stat-badge">📊 Content Length: ${charCount} characters</span>
                        <span class="stat-badge">📝 ${wordCount} words</span>
                    </div>
                    <div class="chunk-text" id="chunkContent">
                        <pre>${chunkText}</pre>
                    </div>
                    <div class="json-download">
                        <a href="${CHUNK_BASE + encodeURIComponent(getChunkFileName(source))}" target="_blank">
                            📥 Download Full JSON File
                        </a>
                    </div>
                </div>
            `;

            const otherChunks = chunks.filter(c => c.chunk_id !== targetChunkId);
            if (otherChunks.length > 0) {
                html += `
                    <div style="margin-top: 20px;">
                        <details>
                            <summary style="cursor: pointer; font-weight: bold; color: #1976d2; font-size: 1.1rem; padding: 10px; background: #e3f2fd; border-radius: 4px;">
                                📋 Other Chunks in this Report (${otherChunks.length})
                            </summary>
                            <div style="margin-top: 10px;">
                `;
                otherChunks.forEach(chunk => {
                    const preview = chunk.text ? chunk.text.substring(0, 150) + (chunk.text.length > 150 ? '...' : '') : 'No preview';
                    html += `
                        <div class="other-chunk" onclick="window.location.href='?source=${encodeURIComponent(source)}&chunk=${chunk.chunk_id}'">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                                <div>
                                    <strong>${chunk.chunk_id}</strong>
                                    ${chunk.heading ? `- ${chunk.heading}` : ''}
                                    ${chunk.page_start ? `(Page ${chunk.page_start})` : ''}
                                </div>
                                <span style="color: #1976d2; font-size: 0.8rem;">click to view →</span>
                            </div>
                            <div style="font-size: 0.85rem; color: #666; margin-top: 5px; white-space: pre-wrap; word-wrap: break-word;">
                                ${preview}
                            </div>
                        </div>
                    `;
                });
                html += `</div></details></div>`;
            }

            container.innerHTML = html;
        }

        function showAllChunks() {
            if (allChunks.length === 0) { alert('No chunks loaded yet.'); return; }
            const container = document.getElementById('chunkList');
            let html = `<div style="background: #e3f2fd; padding: 10px; border-radius: 4px; margin-bottom: 15px;">
                <h3>📋 All Chunks (${allChunks.length})</h3>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">Click on any chunk to view its full content</p>
            </div>`;
            allChunks.forEach(chunk => {
                const isTarget = chunk.chunk_id === chunkId;
                const textPreview = chunk.text ? chunk.text.substring(0, 300) + (chunk.text.length > 300 ? '...' : '') : 'No text content';
                html += `
                    <div class="chunk-container" style="${isTarget ? 'border: 2px solid #ffc107;' : ''}">
                        <div class="chunk-meta" style="${isTarget ? 'background: #fff3cd;' : ''}">
                            <span class="chunk-meta-item"><strong>Chunk ID:</strong> ${chunk.chunk_id} ${isTarget ? '<span class="badge-highlight">🎯 TARGET</span>' : ''}</span>
                            <span class="chunk-meta-item"><strong>Heading:</strong> ${chunk.heading || 'N/A'}</span>
                            <span class="chunk-meta-item"><strong>Pages:</strong> ${chunk.page_start || 'N/A'} ${chunk.page_end ? `- ${chunk.page_end}` : ''}</span>
                            <span class="chunk-meta-item"><strong>Words:</strong> ${chunk.text ? chunk.text.split(/\s+/).length : 0}</span>
                        </div>
                        <div class="chunk-text" style="${isTarget ? 'background: #fffde7; border: 1px solid #ffc107;' : ''}">
                            <pre style="white-space: pre-wrap; word-wrap: break-word; font-family: inherit; margin: 0; line-height: 1.6;">${textPreview}</pre>
                        </div>
                        <div style="margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap;">
                            <button onclick="window.location.href='?source=${encodeURIComponent(source)}&chunk=${chunk.chunk_id}'" class="btn" style="font-size: 0.8rem; padding: 4px 12px;">
                                🔍 View Full Chunk
                            </button>
                            ${isTarget ? '<span style="color: #856404; font-size: 0.9rem;">🎯 Currently viewing this chunk</span>' : ''}
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        loadChunks();
    </script>
</body>
</html>