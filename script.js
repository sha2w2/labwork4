function findBooks() {
    const query = document.getElementById('bookInput').value;
    const resultsDiv = document.getElementById('results');

    resultsDiv.innerHTML = "Searching...";

    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            resultsDiv.innerHTML = "";

            if (!data.books || data.books.length === 0) {
                resultsDiv.innerHTML = "No books found.";
                return;
            }

            data.books.forEach(book => {
                const title = book.title;
                const authors = book.authors.join(", ");
                const bookLink = book.infoLink;

                const bookElement = document.createElement('div');
                bookElement.className = 'book';
                bookElement.innerHTML = `
        <a href="${bookLink}" target="_blank" style="text-decoration: none; color: #1a73e8; font-size: 1.1em;">
            <strong>${title}</strong>
        </a>
        <br>
        <span style="color: #5f6368;">By: ${authors}</span>
    `;

                resultsDiv.appendChild(bookElement);
            });
        });
}