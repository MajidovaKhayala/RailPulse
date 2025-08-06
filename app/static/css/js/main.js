document.addEventListener('DOMContentLoaded', function() {
    let currentNews = [];
    
    document.getElementById('searchBtn').addEventListener('click', fetchNews);
    document.getElementById('exportBtn').addEventListener('click', exportToPDF);
    
    async function fetchNews() {
        const loading = document.getElementById('loading');
        const newsContainer = document.getElementById('newsContainer');
        const exportBtn = document.getElementById('exportBtn');
        
        loading.style.display = 'block';
        newsContainer.innerHTML = '';
        exportBtn.disabled = true;
        
        try {
            const response = await fetch('/search_news');
            currentNews = await response.json();
            
            if (currentNews.length === 0) {
                newsContainer.innerHTML = '<p>No news found.</p>';
                return;
            }
            
            currentNews.forEach(item => {
                const newsItem = document.createElement('div');
                newsItem.className = 'news-item';
                newsItem.innerHTML = `
                    <h3>${item.title}</h3>
                    <p>${item.summary}</p>
                    <div class="meta">
                        <small>Source: ${new URL(item.source).hostname}</small><br>
                        <small>Date: ${item.date}</small><br>
                        <a href="${item.link}" target="_blank">Read more</a>
                    </div>
                `;
                newsContainer.appendChild(newsItem);
            });
            
            exportBtn.disabled = false;
        } catch (error) {
            newsContainer.innerHTML = '<p>Error fetching news. Please try again.</p>';
            console.error('Error:', error);
        } finally {
            loading.style.display = 'none';
        }
    }
    
    async function exportToPDF() {
        if (currentNews.length === 0) return;
        
        try {
            const response = await fetch('/export_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(currentNews)
            });
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `railway_news_${new Date().toISOString().slice(0,10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Export error:', error);
            alert('Error exporting PDF');
        }
    }
});
