const reviewForm = document.getElementById('review-form');
const reviewList = document.getElementById('review-list');
const reviewStatus = document.getElementById('review-status');
const orderForm = document.getElementById('order-form');
const orderStatus = document.getElementById('order-status');
const reactionButtons = document.querySelectorAll('.reaction-btn');

const apiBase = window.MAISON_API_BASE_URL || '';
const reviews = JSON.parse(localStorage.getItem('maison-reviews') || '[]');
const reactionCounts = JSON.parse(localStorage.getItem('maison-reactions') || '{}');

function renderReviews() {
  if (!reviewList) return;
  reviewList.innerHTML = '';
  if (!reviews.length) {
    reviewList.innerHTML = '<div class="review-item">No reviews yet. Be the first to share your experience.</div>';
    return;
  }

  reviews.forEach((review) => {
    const item = document.createElement('div');
    item.className = 'review-item';
    item.innerHTML = `<strong>${review.product}</strong><br />Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}<br />${review.comment}`;
    reviewList.appendChild(item);
  });
}

function setStatus(target, message) {
  if (target) {
    target.textContent = message;
  }
}

function updateReactionButtons() {
  reactionButtons.forEach((button) => {
    const key = button.getAttribute('data-product');
    const count = reactionCounts[key] || 0;
    button.textContent = `Like (${count})`;
  });
}

if (reviewForm) {
  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const product = document.getElementById('review-product').value;
    const rating = Number(document.getElementById('review-rating').value);
    const comment = document.getElementById('review-comment').value.trim();

    if (!comment) return;

    const formData = new URLSearchParams({ product, rating, comment });
    try {
      const response = await fetch(`${apiBase}/api/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
        body: formData.toString()
      });
      const result = await response.json();
      if (result.success) {
        reviews.unshift({ product, rating, comment });
        localStorage.setItem('maison-reviews', JSON.stringify(reviews));
        renderReviews();
        reviewForm.reset();
        setStatus(reviewStatus, 'Review submitted successfully.');
      } else {
        setStatus(reviewStatus, 'Unable to submit review right now.');
      }
    } catch (error) {
      console.error(error);
      setStatus(reviewStatus, 'Unable to submit review right now.');
    }
  });
}

if (orderForm) {
  orderForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const item = document.getElementById('order-item').value;
    const size = document.getElementById('order-size').value;
    const color = document.getElementById('order-color').value.trim();
    const quantity = document.getElementById('order-quantity').value;
    const phone = document.getElementById('order-phone').value.trim();

    const formData = new URLSearchParams({ item, size, color, quantity, phone });
    try {
      const response = await fetch(`${apiBase}/api/order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
        body: formData.toString()
      });
      const result = await response.json();
      if (result.success) {
        const message = `Hello Maison Boutique, I would like to order ${item}. Size: ${size}. Color: ${color}. Quantity: ${quantity}. Contact: ${phone}.`;
        const encoded = encodeURIComponent(message);
        window.open(`https://wa.me/233540311036?text=${encoded}`, '_blank', 'noopener,noreferrer');
        orderForm.reset();
        setStatus(orderStatus, result.message);
      } else {
        setStatus(orderStatus, 'Order could not be submitted.');
      }
    } catch (error) {
      console.error(error);
      setStatus(orderStatus, 'Order could not be submitted.');
    }
  });
}

reactionButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const key = button.getAttribute('data-product');
    reactionCounts[key] = (reactionCounts[key] || 0) + 1;
    localStorage.setItem('maison-reactions', JSON.stringify(reactionCounts));
    updateReactionButtons();
  });
});

renderReviews();
updateReactionButtons();
