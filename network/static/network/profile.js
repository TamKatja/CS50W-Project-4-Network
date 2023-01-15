document.addEventListener('DOMContentLoaded', function() {

    // Display and hide modals on profile page
    const followingModal = document.querySelector('#following-modal');
    const followersModal = document.querySelector('#followers-modal');
    const profilePictureModal = document.querySelector('#profile-picture-modal');

    document.querySelector('#profile-following-count').addEventListener('click', () => {
        showModal(followingModal);
        closeModal();
    });

    document.querySelector('#profile-followers-count').addEventListener('click', () => {
        showModal(followersModal);
        closeModal();
    });

    document.querySelector('#user-profile-picture').addEventListener('click', () => {
        console.log('click');
        showModal(profilePictureModal);
        closeModal();
    });

    function showModal(modal) {
        modal.classList.add('show');
    }

    function closeModal() {
        const closeBtn = document.querySelectorAll('#modal-close-btn');
        closeBtn.forEach(button => {
            button.addEventListener('click', () => {
                const modalClose = button.dataset.modalClose;
                const modal = document.getElementById(modalClose);
                modal.classList.remove('show');
            });
        });
    }
});
