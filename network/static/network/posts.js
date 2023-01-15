document.addEventListener('DOMContentLoaded', () => {

    // Edit post

    // User clicks 'Edit' button
    // API GET request to retrieve post content
    document.querySelectorAll('#edit-post-btn').forEach(btn => {btn.onclick = () => {
        postId = btn.dataset.id;
        fetch(`post/edit/${postId}`)
        .then(response => response.json())
        .then(postData => {
            console.log(postData);
            editPost(postData);
        })
        .catch(error => console.error(error));
    }});

    function editPost(postData) {
        const postId = postData.id;
        const postContent = postData.content;

        // Generate textarea
        const postContentContainer = document.querySelector(`#post-content[data-id="${postId}"]`);
        postContentContainer.style.display = 'none';
        const editContentContainer = document.querySelector(`#edit-post-content[data-id="${postId}"]`);
        editContentContainer.innerText = postContent;
        editContentContainer.style.display = 'block';

        // Display save button
        const editBtn = document.querySelector(`#edit-post-btn[data-id="${postId}"]`);
        const saveBtn = document.querySelector(`#save-post-btn[data-id="${postId}"]`);
        editBtn.style.display = 'none';
        saveBtn.style.display = 'flex';

        // User clicks save button
        saveBtn.onclick = () => {
            newContent = editContentContainer.value;
            updatePost(postId, newContent);
            
            // Reject blank posts
            if (newContent.trim() == "") {
                editContentContainer.value = postContent;
            } else { 
                postContentContainer.innerText = newContent;
            }
            
            // Reset page after saving 
            postContentContainer.style.display = 'block';
            editContentContainer.style.display = 'none';
            saveBtn.style.display = 'none';
            editBtn.style.display = 'flex';
        }
    }

    function updatePost(postId, newContent) {
        // API PUT request to update post content 
        fetch(`post/edit/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: newContent
            })
        })
        .then(response => console.log(response.json()))
        .then(result => {
            console.log(result);
        })
        .catch(error => console.log(error));
        return false;
    } 
        
    // Like post

    // User clicks 'Like' button (i.e. heart icon)
    document.querySelectorAll('#like-post-btn').forEach(btn => {btn.onclick = () => {
        postId = btn.dataset.id;

        // API PUT request to update post likes
        fetch(`post/like/${postId}`, {
            method: 'PUT',
        })
        .then(response => response.json())
        .then(jsonData => {
            // Save data from response
            console.log(jsonData)
            const postLiked = jsonData['post_liked'];
            const likeCount = jsonData['like_count'];

            const likeBtn = document.querySelector(`#like-post-btn[data-id="${postId}"]`);

            // If user has already liked post, unlike post
            if (postLiked) {
                likeBtn.querySelector('span').innerText = 'favorite';
            } else {
                likeBtn.querySelector('span').innerHTML = 'favorite_border';
            }
            
            // Update post like count
            const likeCountContainer = document.querySelector(`#post-like-count[data-id="${postId}"]`);
            likeCountContainer.innerText = likeCount;
        })
        .catch(error => console.error(error));
     }});
});