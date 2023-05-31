const articlesPerPage = 9; // Number of articles to display per page
let currentPage = 1; // Initially show the first page
let articles; // Declare the articles variable outside the function scope
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
const pageCountElement = document.getElementById('page-count'); // Element to display the page count

// Function to display articles based on the current page
function displayArticles() {
  const articleContainer = document.getElementById('article-container');
  articles = articleContainer.getElementsByClassName('article-card');

  for (let i = 0; i < articles.length; i++) {
    articles[i].style.display = 'none';
  }

  const startIndex = (currentPage - 1) * articlesPerPage;
  const endIndex = Math.min(startIndex + articlesPerPage, articles.length);

  for (let i = startIndex; i < endIndex; i++) {
    articles[i].style.display = 'grid';
  }
}

// Function to navigate to the previous page
function goToPrevPage() {
  if (currentPage > 1) {
    currentPage--;
    displayArticles();
    updatePaginationButtons();
    scrollToTop();
  }
}

// Function to navigate to the next page
function goToNextPage() {
  const startIndex = currentPage * articlesPerPage;
  const endIndex = Math.min(startIndex + articlesPerPage, articles.length);

  if (endIndex > startIndex) {
    currentPage++;
    displayArticles();
    updatePaginationButtons();
    scrollToTop();
  }
}

// Function to update the state of pagination buttons
function updatePaginationButtons() {
  prevButton.disabled = currentPage === 1;
  nextButton.disabled = currentPage * articlesPerPage >= articles.length;

  // Calculate the total number of pages
  const pageCount = Math.ceil(articles.length / articlesPerPage);

  // Update the page count element
  pageCountElement.textContent = `Page ${currentPage} sur ${pageCount}`;
}

// Function to scroll to the top of the page with a delay and change cursor
function scrollToTop() {
  // Change cursor to "wait"
  document.body.classList.add('wait-cursor');
  prevButton.style.cursor = 'wait';
  nextButton.style.cursor = 'wait';
  setTimeout(function() {
    window.scrollTo({
      top: 0,
    });

    // Change cursor back to default
    document.body.classList.remove('wait-cursor');
    prevButton.style.cursor = prevButton.disabled ? 'not-allowed' : 'pointer';
    nextButton.style.cursor = nextButton.disabled ? 'not-allowed' : 'pointer';
  }, 1500); // Adjust the delay (in milliseconds) as needed
}

// Attach event listeners to pagination buttons
document.getElementById('prev-button').addEventListener('click', goToPrevPage);
document.getElementById('next-button').addEventListener('click', goToNextPage);

// Initial setup
displayArticles();
updatePaginationButtons();
