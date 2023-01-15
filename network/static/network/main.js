document.addEventListener('DOMContentLoaded', function() {

    // Hide loader once page fully loaded
    const loader = document.querySelector('.loader');
    window.addEventListener('load', () => {
        loader.classList.add('loader-hidden');
    });

    // While no user input, disable 'Post' button (on homepage)
    const newPostContent = document.querySelector('#new-post-content-field');
    if (newPostContent) {
        const postBtn = document.querySelector('#post-btn');
        // Listen for user input
        newPostContent.addEventListener('input', () => {
            if (newPostContent.value.trim() == "") {
                postBtn.disabled = true;
            } else {
                postBtn.disabled = false;
            }
        });
    }
});